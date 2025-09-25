from django.urls import path
from . import views

urlpatterns = [
    path("predict/", views.predict_churn, name="predict_churn"),
    path("predict_csv/", views.predict_csv, name="predict_csv"),  # 🚀 importante
]
