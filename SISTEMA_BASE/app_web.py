import os
import cv2
import numpy as np
import streamlit as st
from PIL import Image
from ultralytics import YOLO

# Rutas a los modelos
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RUTA_DETECTOR = os.path.join(BASE_DIR, "ojos_detector.pt")
RUTA_PEPINO = os.path.join(BASE_DIR, "..", "IA_PEPINO", "cerebro_pepino_v1.pt")
RUTA_PIMIENTO = os.path.join(BASE_DIR, "..", "IA_PIMIENTO", "cerebro_pimiento_v1.pt")

# Diccionarios de traducción según hortaliza
CLASES_PEPINO = {
    "Downy_mildew": "Mildiú (Downy Mildew)",
    "Powdery_mildew": "Oídio (Powdery Mildew)",
    "Healthy_leaves": "Hoja Sana"
}

CLASES_PIMIENTO = {
    "Powdery_mildew": "Oídio (Ceniza)",
    "Thrips_parvispinus": "Thrips (Plaga)",
    "Healthy_leaves": "Hoja Sana",
    "Healthy": "Hoja Sana"
}

st.set_page_config(page_title="AgroVision AI", layout="wide")

st.title("🌱 AgroVision AI: Diagnóstico Fitosanitario")
st.markdown("Herramienta de Computer Vision para la detección de patologías específicas en hoja mediante redes neuronales convolucionales.")

# Selector de cultivo
cultivo = st.selectbox(
    "Selecciona el cultivo que vas a analizar:",
    ("Pepino", "Pimiento")
)

# Información de patologías detectables
if cultivo == "Pepino":
    st.info("📋 **Patologías detectables en Pepino:** Mildiú (`Downy_mildew`), Oídio (`Powdery_mildew`) y Hoja Sana (`Healthy_leaves`).")
    ruta_modelo = RUTA_PEPINO
    dicc_traduccion = CLASES_PEPINO
else:
    st.info("📋 **Patologías detectables en Pimiento:** Oídio (`Powdery_mildew`), Thrips (`Thrips_parvispinus`) y Hoja Sana (`Healthy_leaves`).")
    ruta_modelo = RUTA_PIMIENTO
    dicc_traduccion = CLASES_PIMIENTO

col1, col2 = st.columns([1, 1])

with col1:
    archivo_subido = st.file_uploader(
        f"Arrastra o selecciona una foto de hoja de {cultivo.lower()}:", 
        type=["jpg", "jpeg", "png"]
    )
    
    if archivo_subido is not None:
        imagen_pil = Image.open(archivo_subido)
        st.image(imagen_pil, caption=f"Imagen cargada ({cultivo})", use_container_width=True)

with col2:
    if archivo_subido is not None:
        st.subheader("Resultado del Diagnóstico")
        
        if st.button("🔍 Ejecutar Análisis", type="primary"):
            with st.spinner("Procesando imagen con modelo YOLO..."):
                if not os.path.exists(ruta_modelo):
                    st.error(f"No se encuentra el modelo entrenado en: {ruta_modelo}")
                else:
                    # Cargar modelo clasificador
                    clasificador = YOLO(ruta_modelo)
                    
                    # Cargar imagen en OpenCV
                    img_np = np.array(imagen_pil)
                    img_cv = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)

                    # Inferencia de clasificación directa
                    res = clasificador(img_cv, verbose=False)
                    top1_idx = res[0].probs.top1
                    confianza = res[0].probs.top1conf.item() * 100
                    clase_raw = res[0].names[top1_idx]
                    diagnostico = dicc_traduccion.get(clase_raw, clase_raw)

                    # Tarjeta de resultado
                    if "Sana" in diagnostico or "Healthy" in diagnostico:
                        st.success(f"### Estado: {diagnostico}")
                    else:
                        st.error(f"### Patología detectada: {diagnostico}")
                        
                    st.metric(label="Nivel de Confianza del Modelo", value=f"{confianza:.2f}%")
                    
                    # Recomendación básica
                    if "Oídio" in diagnostico or "Powdery" in diagnostico:
                        st.warning("⚠️ **Acción:** Tratamiento fungicida antioídio (p. ej. azufre) y ventilar el invernadero para bajar humedad.")
                    elif "Mildiú" in diagnostico or "Downy" in diagnostico:
                        st.warning("⚠️ **Acción:** Tratamiento con fungicida específico para mildiú y control estricto de condensación en cubierta.")
                    elif "Thrips" in diagnostico:
                        st.warning("⚠️ **Acción:** Suelta de fauna auxiliar (*Orius laevigatus*) o insecticida autorizado.")
                    else:
                        st.info("Planta en estado óptimo. No requiere tratamiento.")