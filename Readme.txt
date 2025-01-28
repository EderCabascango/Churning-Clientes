# CHURNING - DESERCIÓN DE CLIENTES

## Descripción

Este proyecto tiene como objetivo predecir la deserción de clientes (churn) utilizando un conjunto de datos etiquetado. Se entrena un algoritmo de aprendizaje automático para identificar clientes con alto riesgo de cancelar el servicio. 

## Contexto

El churning, o "tasa de cancelación", se refiere al proceso por el cual los clientes dejan de usar un producto o servicio en un período de tiempo determinado. Es una métrica clave en industrias como telecomunicaciones, banca, suscripciones en línea, servicios SaaS, entre otras.

El churn es crucial porque adquirir un nuevo cliente es mucho más costoso que retener a uno existente. Además, un churn alto indica posibles problemas con el producto, servicio o experiencia del cliente.

Por lo cual este proyecto puede servir como guía para posibles implementaciones en ISPs o diferentes tipos de empresas que ofrecen un servicio de tecnología.

## Metodología

1. **Instanciar e Importar:** Se importan las bibliotecas necesarias (pandas, seaborn, sklearn, etc.) y se carga el conjunto de datos.
2. **EDA - Análisis Exploratorio de Datos:** Se realiza un análisis exploratorio de los datos para comprender su estructura, identificar valores faltantes y detectar posibles sesgos o outliers.
3. **Preprocesamiento de Datos:** Se imputan valores faltantes, se escalan las variables numéricas y se codifican las variables categóricas.
4. **División de Datos:** Se divide el conjunto de datos en conjuntos de entrenamiento y prueba.
5. **Entrenamiento:** Se entrenan diferentes modelos de aprendizaje automático (Regresión Logística, SVM, Árbol de Decisión, Random Forest).
6. **Evaluación:** Se evalúa el rendimiento de los modelos utilizando métricas como la precisión (accuracy), la matriz de confusión y el informe de clasificación.
7. **Testeo:** Se aplica el modelo seleccionado a un conjunto de datos de prueba para evaluar su capacidad de generalización.
8. **Conclusiones:** Se resumen los hallazgos del proyecto y se discuten las limitaciones y posibles mejoras.

## Resultados

* El modelo de Regresión Logística obtuvo el mejor accuracy (0.81) y un buen f1 score.
* La variable "contract" (contrato) tiene mayor relevancia en la predicción del churn.
* El modelo funciona bien en general, pero podría mejorar en la identificación de la clase 1 (clientes que sí desertan).

## Consideraciones

* Se debe tener en cuenta el desbalance de clases en la variable objetivo ("Churn").
* La elección de escaladores o normalizadores puede influir en los resultados.
* Se recomienda realizar cross-validation y Grid Search para optimizar los modelos.

## Autor

Realizado por: Wladimir Cabascango
* Fecha: 27-01-2025
* Email: wladimireder@gmail.com
* Contacto: +593939008880
* LinkedIn: www.linkedin.com/in/wladimir-cabascango-velásquez-79b79810a