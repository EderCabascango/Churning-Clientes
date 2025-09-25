import joblib
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "churn_api", "models", "churn_logreg_pipeline.pkl")

print("Ruta buscada:", MODEL_PATH)

model = joblib.load(MODEL_PATH)

print("Modelo cargado con éxito:", type(model))

if hasattr(model, "feature_names_in_"):
    print("Columnas esperadas:", model.feature_names_in_)
else:
    print("El modelo no tiene atributo 'feature_names_in_'")
    if hasattr(model, "named_steps"):
        print("Pasos del pipeline:", model.named_steps.keys())
