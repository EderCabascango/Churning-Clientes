# ============================================================
# 1. Importar librerías
# ============================================================
import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LogisticRegression
from imblearn.over_sampling import SMOTE
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report, roc_auc_score
import joblib

# ============================================================
# 2. Cargar dataset
# ============================================================
df = pd.read_csv("Churn.csv")

# --- LIMPIEZA de TotalCharges ---
df["TotalCharges"] = df["TotalCharges"].astype(str).str.strip()
df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce").fillna(0)

# Convertir target a binario
df["Churn"] = df["Churn"].map({"No": 0, "Yes": 1})

# Separar variables
X = df.drop(["Churn", "customerID"], axis=1)
y = df["Churn"]


# ============================================================
# 3. Dividir datos
# ============================================================
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42, stratify=y
)

# ============================================================
# 4. Identificar columnas (forzamos TotalCharges como numérica)
# ============================================================
num_cols = ["tenure", "MonthlyCharges", "TotalCharges"]
cat_cols = [c for c in X_train.columns if c not in num_cols]

print("DEBUG num_cols:", num_cols)
print("DEBUG cat_cols:", cat_cols)

# Preprocesador
preprocessor = ColumnTransformer(
    transformers=[
        ("num", StandardScaler(), num_cols),
        ("cat", OneHotEncoder(handle_unknown="ignore"), cat_cols),
    ]
)

# ============================================================
# 5. Transformar X_train para aplicar SMOTE
# ============================================================
X_train_encoded = preprocessor.fit_transform(X_train)

smote = SMOTE(random_state=42)
X_resampled, y_resampled = smote.fit_resample(X_train_encoded, y_train)

# ============================================================
# 6. Entrenar clasificador con GridSearch
# ============================================================
clf = LogisticRegression(max_iter=500, random_state=42)

param_grid = {
    "C": [0.01, 0.1, 1, 10],
    "penalty": ["l1", "l2"],
    "solver": ["liblinear", "saga"]
}

grid = GridSearchCV(
    estimator=clf,
    param_grid=param_grid,
    scoring="f1",
    cv=5,
    n_jobs=-1,
    verbose=2
)

grid.fit(X_resampled, y_resampled)

print("Mejores parámetros:", grid.best_params_)
print("Mejor score en CV:", grid.best_score_)

# ============================================================
# 7. Evaluar en test
# ============================================================
X_test_encoded = preprocessor.transform(X_test)

best_clf = grid.best_estimator_
y_pred = best_clf.predict(X_test_encoded)

print("\n📊 Classification Report:")
print(classification_report(y_test, y_pred))
print("ROC-AUC:", roc_auc_score(y_test, best_clf.predict_proba(X_test_encoded)[:, 1]))

# ============================================================
# 8. Guardar pipeline FINAL
# ============================================================
final_pipeline = Pipeline(steps=[
    ("preprocessor", preprocessor),
    ("classifier", best_clf)
])

joblib.dump(final_pipeline, "churn_logreg_pipeline.pkl")
print("\n✅ Modelo guardado en 'churn_logreg_pipeline.pkl'")
