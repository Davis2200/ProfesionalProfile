# 🤖 Artefactos y Serialización de Machine Learning (`/models`)

Este directorio almacena los componentes binarios y lógicos del pipeline de modelado predictivo. Estos archivos representan el estado entrenado y calibrado del sistema, permitiendo que la aplicación web (`app.py`) realice inferencias de riesgo en tiempo real de manera reproducible y con baja latencia, sin necesidad de reentrenar el algoritmo en cada consulta.

---

## 📦 Inventario de Artefactos

El directorio se compone de dos archivos críticos que trabajan en un esquema de **pipeline secuencial**:

### 1. `scaler_model.pkl` (1.20 KB)
* **Tecnología:** Objeto de la clase `StandardScaler` de Scikit-Learn, serializado mediante `joblib`.
* **Propósito:** Almacenar de manera persistente la media ($\mu$) y la desviación estándar ($\sigma$) calculadas sobre el set de datos con ingeniería de variables original (`features_engineered.csv`).
* **Importancia en Producción:** Evita el sesgo por desalineación de datos (*Data Drift*). Cada vez que un usuario interactúe con el *Live Risk Simulator* e ingrese un perfil crudo, este archivo se encarga de estandarizar los valores numéricos para que coincidan exactamente con la escala que el modelo XGBoost espera recibir.

### 2. `modelo_fuga_final.json` (986.9 KB)
* **Tecnología:** Estructura serializada nativa de **XGBoost Classifier** (`xgb.XGBClassifier`).
* **Propósito:** Contiene la arquitectura lógica de los 500 árboles de decisión, las condiciones de división de nodos (*splits*) y los pesos asignados a las hojas (*leaves*) para calcular la probabilidad exacta de abandono.
* **Propiedades del Modelo Guardado:**
    * **Arquitectura:** Árboles limitados a una profundidad máxima de 4 (`max_depth=4`) para prevenir la memorización del ruido estocástico.
    * **Penalización:** Incorpora regularización L2 (`reg_lambda=10`) y costo de división (`gamma=1`).
    * **Estrategia Inversa de Pesos:** Guarda la matriz ajustada por el parámetro `scale_pos_weight` (proporción matemática entre clientes retenidos y en fuga), equilibrando el gradiente para penalizar con mayor severidad los errores en la clase minoritaria.

---

## ⚙️ Flujo de Consumo en la Capa de Inferencia (`Inference Flow`)

La aplicación interactiva ejecuta de manera síncrona los artefactos en el siguiente orden estricto: