# 🌱 AgroVision AI: Computer Vision para Diagnóstico Fitosanitario

Sistema de visión por computador basado en Deep Learning (YOLOv8) para la detección y clasificación automatizada de patologías en hojas de cultivo intensivo en invernadero (Pepino y Pimiento).

---

## 🚀 Demo Interactiva en Vivo
Prueba el sistema en tiempo real directamente desde el navegador (sin instalación):  
👉 **[Abrir AgroVision AI en Streamlit Cloud](https://agrovision-demo.streamlit.app/)**

---

## 📋 Patologías y Plagas Soportadas

### 🥒 Cultivo de Pepino (*Cucumis sativus*)
- **Mildiú** (*Pseudoperonospora cubensis*)
- **Oídio / Ceniza** (*Podosphaera fusca*)
- **Tejido Vegetal Sano** (*Healthy Leaves*)

### 🫑 Cultivo de Pimiento (*Capsicum annuum*)
- **Oídio / Ceniza** (*Leveillula taurica*)
- **Thrips** (*Thrips parvispinus*)
- **Tejido Vegetal Sano** (*Healthy Leaves*)

---

## 🛠️ Stack Tecnológico
- **Arquitectura de Visión:** Ultralytics YOLOv8 (Transfer Learning y Fine-Tuning específico).
- **Procesamiento Digital de Imágenes:** OpenCV (`opencv-python-headless`) y PIL (Pillow).
- **Frontend y Cloud Deployment:** Streamlit Community Cloud.
- **Gestión de Model Weights:** Git LFS (Large File Storage).

---

## 💻 Ejecución en Local (Opcional)

Si deseas clonar y ejecutar el entorno en local:

```bash
# 1. Clonar el repositorio
git clone [https://github.com/Mgalex2006/agrovision-demo.git](https://github.com/Mgalex2006/agrovision-demo.git)
cd agrovision-demo

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Ejecutar la aplicación web
streamlit run SISTEMA_BASE/app_web.py
