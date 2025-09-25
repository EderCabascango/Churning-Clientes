import os
import joblib
import pandas as pd
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
import json

# ==========================================
# Cargar el modelo entrenado
# ==========================================
MODEL_PATH = os.path.join(settings.BASE_DIR, "models", "churn_logreg_pipeline.pkl")
model = joblib.load(MODEL_PATH)


# ==========================================
# Función de limpieza de datos
# ==========================================
def clean_dataframe(df):
    # Limpieza de TotalCharges
    if "TotalCharges" in df.columns:
        df["TotalCharges"] = df["TotalCharges"].astype(str).str.strip()
        df["TotalCharges"] = df["TotalCharges"].replace({"": "0", "nan": "0", "None": "0"})
        df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce").fillna(0.0)

    # Convertir columnas numéricas
    numeric_cols = ["tenure", "MonthlyCharges", "TotalCharges"]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

    # Convertir categóricas a string
    categorical_columns = [
        "gender", "SeniorCitizen", "Partner", "Dependents", "PhoneService", "MultipleLines",
        "InternetService", "OnlineSecurity", "OnlineBackup", "DeviceProtection",
        "TechSupport", "StreamingTV", "StreamingMovies", "Contract",
        "PaperlessBilling", "PaymentMethod"
    ]
    for col in categorical_columns:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip().fillna("Unknown")

    return df


# ==========================================
# Endpoint: predecir un cliente (JSON)
# ==========================================
@csrf_exempt
def predict_churn(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body.decode("utf-8"))
            df = pd.DataFrame([data])
            df = clean_dataframe(df)

            # Reordenar columnas según entrenamiento
            expected_cols = (
                model.named_steps['preprocessor'].transformers_[0][2] +
                model.named_steps['preprocessor'].transformers_[1][2]
            )
            df = df[expected_cols]

            # Predicción
            prediction = model.predict(df)[0]
            probability = model.predict_proba(df)[0][1]

            return JsonResponse({
                "prediction": int(prediction),
                "probability": float(probability)
            })

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "Only POST method allowed"}, status=405)


# ==========================================
# Endpoint: predecir desde CSV
# ==========================================
@csrf_exempt
def predict_csv(request):
    if request.method == "POST":
        try:
            # Guardar archivo temporal
            file = request.FILES["file"]
            file_path = default_storage.save("tmp/" + file.name, file)

            # Leer CSV
            df = pd.read_csv(os.path.join(settings.MEDIA_ROOT, file_path))
            df = clean_dataframe(df)

            # Reordenar columnas según entrenamiento
            expected_cols = (
                model.named_steps['preprocessor'].transformers_[0][2] +
                model.named_steps['preprocessor'].transformers_[1][2]
            )
            df = df[expected_cols]

            # Predicciones
            preds = model.predict(df)
            probs = model.predict_proba(df)[:, 1]

            results = [
                {
                    "index": i,
                    "prediction": int(preds[i]),
                    "probability": float(probs[i])
                }
                for i in range(len(df))
            ]

            return JsonResponse({"results": results})

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "Only POST method allowed"}, status=405)
