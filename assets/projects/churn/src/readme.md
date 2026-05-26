# ⚙️ Módulos del Núcleo del Software (`/src`)

Este directorio contiene los componentes lógicos y las utilidades de automatización que estructuran el pipeline de Machine Learning del **Banking Churn Predictive System**. La arquitectura del código está diseñada bajo principios de modularidad, separando la generación de datos simulados, el pivoteo y cálculo de KPIs, la normalización estadística y el entrenamiento optimizado del algoritmo.

---

## 🗂️ Mapeo del Directorio

| Archivo | Rol en el Pipeline | Tipo de Operación | Salidas Generadas |
| :--- | :--- | :--- | :--- |
| `data.py` | Simulador e Ingesta de Datos | Generación Estocástica | `banca_transacciones.csv` |
| `features.py` | Ingeniería de Características | Agregación y Modelado Lineal | `features_engineered.csv` |
| `scaler.py` | Estandarización Estadística | Preprocesamiento | `features_scaled.csv`, `scaler_model.pkl` |
| `model.py` | Optimización y Entrenamiento | Modelado Predictivo | `modelo_fuga_final.json` |

---

## 🔍 Análisis Detallado de Código

### 1. Ingesta y Simulación Estocástica (`data.py`)
Este script actúa como el motor de simulación sintética del comportamiento bancario para un universo de $120,000$ clientes durante un horizonte temporal de 6 meses (`t-5` a `t`). 

* **Lógica de Negocio Integrada:** En lugar de asignar un comportamiento aleatorio uniforme, implementa una **Distribución Beta** `np.random.beta(2, 5)` para simular un *Índice de Propensión de Fuga*. Esto asegura un comportamiento asimétrico realista: la mayoría de los clientes son estables y leales, mientras que una minoría presenta alta propensión al abandono.
* **Degradación Temporal:** Si el índice de propensión de un cliente supera el umbral crítico de $0.6$ en los últimos meses del ciclo (`idx > 3`), el script induce un algoritmo de degradación que reduce orgánicamente el saldo, disminuye drásticamente el volumen de transacciones (`num_trx`), simula la pérdida de la portabilidad de nómina y aumenta las quejas mediante una **Distribución de Poisson**.
* **Ruido en el Target:** El `target_fuga` definitivo ($0$ o $1$) se genera añadiendo ruido blanco al índice para evitar correlaciones perfectas lineales, forzando al modelo a aprender patrones verdaderamente complejos.

---

### 2. Pivoteo e Ingeniería de Características de Alto Valor (`features.py`)
Transforma el dataset de formato largo (múltiples filas por cliente) a formato ancho (una sola fila resumen por cliente) y extrae indicadores de valor predictivo avanzado.

* **Cálculo de Tendencias mediante Regresión Lineal (`calcular_pendiente`):** Utiliza `LinearRegression` de Scikit-Learn para ajustar dinámicamente una línea de tendencia sobre el volumen de transacciones de cada cliente a lo largo de los 6 meses. La pendiente resultante determina numéricamente si el cliente está entrando en un estado de inactividad (*dormancy*).
* **KPIs Extraídos en `construir_features_alto_valor`:**
    * `ratio_saldo_3m`: Ratio entre el saldo del último mes (`t`) versus el promedio del trimestre anterior. Captura fugas de capital sutiles.
    * `pendiente_actividad`: Coeficiente de la regresión que mide la aceleración o desaceleración transaccional.
    * `shifter_nomina`: Variable binaria (*Trigger Event*) que detecta si el cliente canceló su cuenta de nómina entre el mes `t-1` y `t`.
    * `volatilidad_transaccional`: Coeficiente de variación (desviación estándar / media) para detectar anomalías en la frecuencia de uso.
    * `friccion_ponderada`: Índice acumulado de reclamos que castiga el comportamiento reciente aplicando pesos ponderados (`quejas_t * 3` + `quejas_t-1 * 1.5`).

---

### 3. Estandarización y Preservación del Estado (`scaler.py`)
Módulo encargado de garantizar la homogeneidad dimensional de las variables cuantitativas creadas por el pipeline anterior.

* **Estandarización Z-Score:** Implementa `StandardScaler` para reescalar las características de modo que cada columna tenga una media ($\mu = 0$) y una desviación estándar ($\sigma = 1$). Esto evita que variables con magnitudes nominales muy altas (como los saldos) eclipsen el peso de variables con rangos pequeños (como las pendientes o variables binarias).
* **Preservación del Objeto (`scaler_model.pkl`):** Mediante `joblib`, se exporta el estado interno del escalador (`fit_transform`). **Este paso es mandatorio para producción:** la interfaz web (`app.py`) requiere este archivo binario para transformar los datos crudos de nuevos usuarios con las mismas medias y varianzas con las que se entrenó el modelo XGBoost, evitando discrepancias en la inferencia (*Data Drift*).

---

### 4. Entrenamiento y Configuración Anti-Sobreajuste (`model.py`)
El script principal de modelado implementa un clasificador **XGBoost (Gradient Boosting)** optimizado para entornos desbalanceados.

* **Manejo del Desbalanceo Extremo:** Configura dinámicamente el parámetro `scale_pos_weight` calculando el ratio matemático exacto entre la clase mayoritaria (clientes retenidos) y la minoritaria (clientes en fuga): 
    $$\text{scale\_pos\_weight} = \frac{\text{len}(y) - \sum y}{\sum y}$$
* **Control Estricto de Sobreajuste (Overfitting):**
    * `max_depth=4`: Árboles poco profundos para evitar la memorización del ruido de simulación.
    * `learning_rate=0.05`: Tasa de aprendizaje baja combinada con `n_estimators=500` para una convergencia suave y robusta.
    * `early_stopping_rounds=20`: Si la métrica de pérdida (`logloss`) en el set de prueba (`X_test`) deja de mejorar durante 20 iteraciones continuas, el entrenamiento se congela automáticamente.
    * Reguladores `reg_lambda=10` y `gamma=1` para penalizar la complejidad estructural del modelo.
* **Salidas de Evaluación:** Imprime el reporte de clasificación (Métricas de precisión, recall y F1-Score) y calcula el **ROC-AUC Score (0.85)** antes de exportar el archivo nativo de producción `modelo_fuga_final.json`.

---

## 🧬 Flujo Secuencial de Ejecución

Para ejecutar el pipeline completo de este directorio de forma manual, ejecute los comandos en el siguiente orden desde la consola:

```bash
# 1. Generar base de datos simulada
python src/data.py

# 2. Transformar y construir KPIs
python src/features.py

# 3. Aplicar escalamiento estadístico y guardar el transformador
python src/scaler.py

# 4. Entrenar, evaluar y exportar el modelo clasificador
python src/model.py