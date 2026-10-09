import os
import cv2
import csv
import random
from datetime import datetime
import numpy as np
import streamlit as st
from PIL import Image
from ultralytics import YOLO
import folium
from streamlit_folium import st_folium

# --- CONFIGURACIÓN DE RUTAS ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RUTA_PEPINO = os.path.join(BASE_DIR, "..", "IA_PEPINO", "cerebro_pepino_v1.pt")
RUTA_PIMIENTO = os.path.join(BASE_DIR, "..", "IA_PIMIENTO", "cerebro_pimiento_v1.pt")
ARCHIVO_DB = os.path.join(BASE_DIR, "historial_plagas.csv")

# Fallback de rutas si los modelos están en la raíz
if not os.path.exists(RUTA_PEPINO):
    RUTA_PEPINO = os.path.join(BASE_DIR, "cerebro_pepino_v1.pt")
if not os.path.exists(RUTA_PIMIENTO):
    RUTA_PIMIENTO = os.path.join(BASE_DIR, "cerebro_pimiento_v1.pt")

# Diccionarios de clases
CLASES_PEPINO = {
    "Downy_mildew": "Mildiú",
    "Powdery_mildew": "Oídio (Ceniza)",
    "Healthy_leaves": "SANA"
}

CLASES_PIMIENTO = {
    "Powdery_mildew": "Oídio (Ceniza)",
    "Thrips_parvispinus": "THRIPS",
    "Healthy_leaves": "SANA",
    "Healthy": "SANA"
}

# --- GESTIÓN DE BASE DE DATOS (CSV) ---
def guardar_en_historial(enfermedad, lat, lon):
    existe = os.path.isfile(ARCHIVO_DB)
    with open(ARCHIVO_DB, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        if not existe:
            writer.writerow(["FECHA", "HORA", "ENFERMEDAD", "LATITUD", "LONGITUD"])
        ahora = datetime.now()
        writer.writerow([
            ahora.strftime("%Y-%m-%d"),
            ahora.strftime("%H:%M:%S"),
            enfermedad,
            round(lat, 6),
            round(lon, 6)
        ])

def leer_historial():
    puntos = []
    if os.path.isfile(ARCHIVO_DB):
        with open(ARCHIVO_DB, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                try:
                    puntos.append(row)
                except Exception:
                    pass
    return puntos

# --- SIMULADOR DE TELEMETRÍA Y GPS ---
def obtener_coordenadas_muestra():
    # Coordenadas base en zona agrícola intensiva (El Ejido)
    lat_base = 36.7725
    lon_base = -2.8140
    lat_actual = lat_base + random.uniform(-0.005, 0.005)
    lon_actual = lon_base + random.uniform(-0.005, 0.005)
    return lat_actual, lon_actual

# --- GENERADOR DEL MAPA EPIDEMIOLÓGICO ---
def crear_mapa(lat_centro, lon_centro, historial):
    mapa = folium.Map(
        location=[lat_centro, lon_centro],
        zoom_start=15,
        tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
        attr='Esri Satellite'
    )
    
    colores = {
        "SANA": "green",
        "Oídio (Ceniza)": "orange",
        "Mildiú": "purple",
        "THRIPS": "red"
    }

    for p in historial:
        enf = p.get("ENFERMEDAD", "Desconocido")
        color = colores.get(enf, "blue")
        popup_html = f"<b>{enf}</b><br>Fecha: {p.get('FECHA')}<br>Hora: {p.get('HORA')}"
        folium.Marker(
            location=[float(p["LATITUD"]), float(p["LONGITUD"])],
            popup=popup_html,
            tooltip=f"{enf} ({p.get('FECHA')})",
            icon=folium.Icon(color=color, icon="info-sign")
        ).add_to(mapa)

    return mapa

# --- INTERFAZ STREAMLIT ---
st.set_page_config(page_title="AgroVision AI - Red Fitosanitaria", layout="wide")

st.title("🌱 AgroVision AI: Diagnóstico y Mapa Epidemiológico en Tiempo Real")
st.markdown("Plataforma colaborativa de detección fitosanitaria. Los diagnósticos confirmados se geoposicionan automáticamente para alerta comunitaria entre explotaciones colindantes.")

# Selector de cultivo
cultivo = st.selectbox("Selecciona cultivo a inspeccionar:", ("Pepino", "Pimiento"))

if cultivo == "Pepino":
    st.info("📋 **Patologías registrables en Pepino:** Mildiú (`Downy_mildew`), Oídio (`Powdery_mildew`) y Hoja Sana (`Healthy_leaves`).")
    ruta_modelo = RUTA_PEPINO
    dicc = CLASES_PEPINO
else:
    st.info("📋 **Patologías registrables en Pimiento:** Oídio (`Powdery_mildew`), Thrips (`Thrips_parvispinus`) y Hoja Sana (`Healthy_leaves`).")
    ruta_modelo = RUTA_PIMIENTO
    dicc = CLASES_PIMIENTO

col1, col2 = st.columns([1, 1])

# Estado de sesión para persistir mapa tras análisis
if "ultima_deteccion" not in st.session_state:
    st.session_state.ultima_deteccion = None

with col1:
    archivo_subido = st.file_uploader(
        f"Cargar imagen de hoja de {cultivo.lower()}:",
        type=["jpg", "jpeg", "png"]
    )
    
    if archivo_subido is not None:
        img_pil = Image.open(archivo_subido)
        st.image(img_pil, caption=f"Muestra: {cultivo}", use_container_width=True)

        if st.button("🔍 Diagnosticar y Geoposicionar", type="primary"):
            with st.spinner("Ejecutando inferencia neuronal..."):
                if not os.path.exists(ruta_modelo):
                    st.error(f"Modelo no disponible en: {ruta_modelo}")
                else:
                    clasificador = YOLO(ruta_modelo)
                    img_cv = cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)
                    
                    res = clasificador(img_cv, verbose=False)
                    top1 = res[0].probs.top1
                    conf = res[0].probs.top1conf.item() * 100
                    clase_raw = res[0].names[top1]
                    diagnostico = dicc.get(clase_raw, clase_raw)

                    # Simular adquisición de GPS en campo
                    lat_gps, lon_gps = obtener_coordenadas_muestra()
                    
                    # Registrar en base de datos epidemiológica
                    guardar_en_historial(diagnostico, lat_gps, lon_gps)
                    
                    st.session_state.ultima_deteccion = {
                        "diagnostico": diagnostico,
                        "confianza": conf,
                        "lat": lat_gps,
                        "lon": lon_gps
                    }

    if st.session_state.ultima_deteccion:
        det = st.session_state.ultima_deteccion
        if "SANA" in det["diagnostico"]:
            st.success(f"### Resultado: Tejido SANO ({det['confianza']:.1f}%)")
        else:
            st.error(f"### ⚠️ Foco detectado: {det['diagnostico']} ({det['confianza']:.1f}%)")
            st.warning(f"📍 Muestra georreferenciada en: Lat {det['lat']:.5f}, Lon {det['lon']:.5f}. Punto añadido al mapa comunitario.")

with col2:
    st.subheader("🗺️ Red Satelital de Incidencias en la Zona")
    st.caption("Pines en el mapa: 🟠 Oídio | 🟣 Mildiú | 🔴 Thrips | 🟢 Sano")
    
    historial = leer_historial()
    
    if st.session_state.ultima_deteccion:
        centro_lat = st.session_state.ultima_deteccion["lat"]
        centro_lon = st.session_state.ultima_deteccion["lon"]
    elif len(historial) > 0:
        centro_lat = float(historial[-1]["LATITUD"])
        centro_lon = float(historial[-1]["LONGITUD"])
    else:
        centro_lat, centro_lon = 36.7725, -2.8140

    mapa_objeto = crear_mapa(centro_lat, centro_lon, historial)
    st_folium(mapa_objeto, width=650, height=520)