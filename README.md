# 🌱 AgroVision AI: Diagnóstico Fitosanitario y Red Epidemiológica Satelital

Plataforma integral de Computer Vision y monitorización geoespacial orientada a agricultura intensiva en invernadero. Combina redes neuronales convolucionales para el diagnóstico foliar en tiempo real con una red epidemiológica georreferenciada para la alerta temprana entre explotaciones agrícolas.

---

## 🚀 Demo Interactiva en Producción
Acceso directo sin instalación ni configuración local:  
👉 **[Probar AgroVision AI en Streamlit Cloud](https://agrovision-demo.streamlit.app/)**

---

## 📋 Capacidades y Patologías Soportadas

### 🥒 Cultivo de Pepino (*Cucumis sativus*)
- **Mildiú** (*Pseudoperonospora cubensis*)
- **Oídio / Ceniza** (*Podosphaera fusca*)
- **Tejido Vegetal Sano** (*Healthy Leaves*)

### 🫑 Cultivo de Pimiento (*Capsicum annuum*)
- **Oídio / Ceniza** (*Leveillula taurica*)
- **Thrips** (*Thrips parvispinus*)
- **Tejido Vegetal Sano** (*Healthy Leaves*)

---

## 🗺️ Arquitectura Epidemiológica y Telemetría
1. **Inferencia Neuronal:** Diagnóstico inmediato de la muestra con porcentaje de confianza.
2. **Georreferenciación GPS:** Adquisición y registro de coordenadas geográficas en el momento de la detección.
3. **Persistencia de Focos:** Registro automatizado de eventos con marca temporal oficial (Europa/Madrid).
4. **Visualización Satelital (GIS):** Integración con mapas satelitales mediante Folium para la detección de focos de infección colindantes en mapas de alta resolución.

---

## 📊 Validación y Métricas del Modelo

Rendimiento del clasificador obtenido sobre el conjunto de validación independiente:

| Matriz de Confusión | Curvas de Aprendizaje y Pérdida |
| :---: | :---: |
| ![Matriz de Confusión](confusion_matrix.png) | ![Resultados](results.png) |

---

## 🛠️ Stack Tecnológico
- **Deep Learning:** Ultralytics YOLOv8 (Transfer Learning y Fine-Tuning específico).
- **Computer Vision:** OpenCV (`opencv-python-headless`) y Pillow (PIL).
- **Geolocalización y Mapas:** Folium, Streamlit-Folium y ArcGIS World Imagery.
- **Frontend & Cloud Hosting:** Streamlit Community Cloud.
- **Control de Versiones y Model Weights:** Git LFS (Large File Storage).

---

## 📄 Licencia y Propiedad Intelectual
El código fuente de la interfaz y la plataforma se distribuye bajo licencia **GNU General Public License v3.0**.  
*Nota: Los datasets de entrenamiento originales y los pipelines de optimización agronómica son propiedad exclusiva del autor.*
