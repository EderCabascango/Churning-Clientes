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
# 4. Identificar columnas
# ============================================================
num_cols = X_train.select_dtypes(include=["int64", "float64"]).columns
cat_cols = X_train.select_dtypes(include=["object"]).columns

# Preprocesamiento: escalar numéricas + one-hot en categóricas
preprocessor = ColumnTransformer(
    transformers=[
        ("num", StandardScaler(), num_cols),
        ("cat", OneHotEncoder(handle_unknown="ignore"), cat_cols),
    ]
)

# ============================================================
# 5. Aplicar SMOTE SOLO en entrenamiento
# ============================================================
smote = SMOTE(random_state=42)
X_resampled, y_resampled = smote.fit_resample(X_train, y_train)

# ============================================================
# 6. Pipeline SOLO con preprocesamiento + modelo
# ============================================================
pipeline = Pipeline(steps=[
    ("preprocessor", preprocessor),
    ("classifier", LogisticRegression(max_iter=500, random_state=42))
])

# ============================================================
# 7. Definir parámetros para GridSearch
# ============================================================
param_grid = {
    "classifier__C": [0.01, 0.1, 1, 10],
    "classifier__penalty": ["l1", "l2"],
    "classifier__solver": ["liblinear", "saga"]
}

grid = GridSearchCV(
    estimator=pipeline,
    param_grid=param_grid,
    scoring="f1",  # métrica adecuada para desbalanceo
    cv=5,
    n_jobs=-1,
    verbose=2
)

# ============================================================
# 8. Entrenar modelo con GridSearch en datos balanceados
# ============================================================
grid.fit(X_resampled, y_resampled)

print("Mejores parámetros:", grid.best_params_)
print("Mejor score en CV:", grid.best_score_)

# ============================================================
# 9. Evaluar en test
# ============================================================
best_model = grid.best_estimator_
y_pred = best_model.predict(X_test)

print("\n📊 Classification Report:")
print(classification_report(y_test, y_pred))
print("ROC-AUC:", roc_auc_score(y_test, best_model.predict_proba(X_test)[:, 1]))

# ============================================================
# 10. Guardar modelo entrenado
# ============================================================
joblib.dump(best_model, "churn_logreg_pipeline.pkl")
print("\n✅ Modelo guardado en 'churn_logreg_pipeline.pkl'")
