# 📌 Fuyu – Churn Prediction App

Este proyecto forma parte del portafolio de **Fuyu** y tiene como objetivo demostrar cómo integrar **Machine Learning en producción** utilizando un stack moderno:

- **Backend:** Django REST Framework que expone modelos entrenados de predicción.
- **Frontend:** Flutter como aplicación multiplataforma (Web/Android/iOS).
- **Modelos incluidos:**
  - **Churn Prediction:** predicción de fuga de clientes en telecomunicaciones.
  - **Stroke Prediction:** prototipo de predicción de accidentes cerebrovasculares.

---

## 🚀 Características principales
- API REST en Django que sirve predicciones en tiempo real.
- Integración con modelos de Machine Learning entrenados en scikit-learn.
- Aplicación Flutter con formulario y carga de CSV para predecir múltiples clientes a la vez.
- Arquitectura modular y lista para escalar.
- Código limpio y estructurado, enfocado en portafolio profesional.

---

## 🛠️ Tecnologías utilizadas
### Backend (Django)
- Python 3.11+
- Django 5.x
- Django REST Framework
- Scikit-learn
- Pandas / Joblib

### Frontend (Flutter)
- Flutter 3.x
- Dart SDK
- HTTP client
- File Picker (para subir CSVs en Web y escritorio)

---

## 📂 Estructura del proyecto
```
/Churning-Clientes
 ├── backend_django/
 │    └── churn_api/
 │         ├── churn/
 │         ├── churn_api/
 │         ├── models/
 │         ├── manage.py
 │         └── requirements.txt
 │
 ├── frontend_flutter/
 │    └── churn_app/
 │         ├── lib/
 │         ├── pubspec.yaml
 │         └── assets/
 │
 ├── Datasets/          # Datasets de ejemplo (sin datos sensibles)
 └── README.md
```

---

## ⚙️ Instalación y ejecución

### 🔹 Backend (Django API)
1. Clonar repositorio:
   ```bash
   git clone https://github.com/EderCabascango/Churning-Clientes.git
   cd Churning-Clientes/backend_django/churn_api
   ```
2. Crear entorno virtual:
   ```bash
   python -m venv venv
   source venv/bin/activate   # Linux/Mac
   venv\Scripts\activate    # Windows
   ```
3. Instalar dependencias:
   ```bash
   pip install -r requirements.txt
   ```
4. Ejecutar servidor:
   ```bash
   python manage.py runserver
   ```
   El backend quedará en: [http://127.0.0.1:8000](http://127.0.0.1:8000)

---

### 🔹 Frontend (Flutter App)
1. Ir al frontend:
   ```bash
   cd ../../frontend_flutter/churn_app
   ```
2. Instalar dependencias:
   ```bash
   flutter pub get
   ```
3. Ejecutar en navegador (Chrome):
   ```bash
   flutter run -d chrome
   ```
4. O en Android/iOS:
   ```bash
   flutter run
   ```

---

## 📊 Ejemplo de uso
- Ingresar datos del cliente en la app Flutter.  
- Enviar la solicitud → la API responde con la predicción:  
  ```json
  {
    "prediction": 1,
    "probability": 0.78
  }
  ```
- También puedes subir un archivo CSV para obtener predicciones por lote.

---

## 🖼️ Logo Fuyu
![Fuyu Logo](assets/fuyu_logo.png)

---

## ✨ Créditos
Desarrollado por **Eder Cabascango** como parte de su portafolio de Ciencia de Datos e Ingeniería en Machine Learning.  
> *“Llevamos tu negocio al futuro” – Fuyu*
