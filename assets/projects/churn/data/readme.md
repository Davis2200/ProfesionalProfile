# 📊 Ingesta, Ciclo de Vida e Ingeniería de Datos (`/data`)

Este directorio funciona como el núcleo de persistencia y almacenamiento analítico del proyecto. Centraliza desde la generación estocástica de los registros transaccionales en bruto hasta las matrices intermedias normalizadas listas para el entrenamiento del modelo XGBoost, garantizando la trazabilidad matemática de cada variable.

---

## 🗃️ Catálogo de Archivos e Infraestructura Tabular

El volumen de datos se compone de tres etapas de maduración distribuidas en los siguientes archivos:

### 1. `banca_transacciones.csv`
* **Tipo de Contenido:** Histórico transaccional crudo en formato largo (*Long Format*).
* **Volumen:** $720,000$ registros individuales (120,000 clientes únicos evaluados a lo largo de un horizonte temporal de 6 meses: `t-5` a `t`).
* **Origen de Datos (Simulación Estocástica):** Este archivo es el resultado directo de la ejecución de `src/data.py`. No contiene datos aleatorios uniformes; fue modelado bajo reglas financieras y probabilísticas estrictas:
    * **Propensión Basada en Distribución Beta:** Se asigna una probabilidad latente a cada usuario mediante $\text{Beta}(2, 5)$, forzando una asimetría derecha realista (donde la gran mayoría de la cartera es leal y solo un porcentaje crítico presenta riesgo).
    * **Degradación Inducida por Umbral:** Si un cliente supera un índice latente de $0.6$ y se encuentra en la ventana de cierre (`idx > 3`), el script gatilla un algoritmo de deterioro que erosiona el saldo real (`saldo_mes`), desploma la frecuencia operativa (`num_trx`), simula la pérdida de la portabilidad de nómina (`tiene_nomina`) e incrementa las quejas mediante una **Distribución de Poisson** ($\lambda = 0.8$).
    * **Ruido Blanco en Target:** La etiqueta final `target_fuga` ($0$ o $1$) se define aplicando ruido gaussiano $\mathcal{N}(0, 0.1)$ sobre un umbral crítico de $0.7$, inyectando la fricción y el solapamiento de patrones característicos de los entornos de producción reales.

### 2. `features_engineered.csv`
* **Tipo de Contenido:** Matriz consolidada de indicadores de negocio en formato ancho (*Wide Format*).
* **Estructura:** $120,000$ filas (una por cliente único). Convierte las series de tiempo mensuales en 6 KPIs de alto valor predictivo mediante el pivoteo y la ejecución de modelos lineales internos (`features.py`).
* **Variables Clave Extraídas:**
    * `ratio_saldo_3m`: Tasa de descapitalización del último trimestre.
    * `pendiente_actividad`: Coeficiente analítico (gradiente) de la regresión lineal sobre el volumen de transacciones.
    * `shifter_nomina`: Flag binario de interrupción súbita del depósito de nómina (evento detonante).
    * `volatilidad_transaccional`: Coeficiente de variación ($\sigma / \mu$) del uso de canales.
    * `friccion_ponderada`: Índice de quejas acumuladas que castiga con mayor peso el comportamiento reciente (`quejas_t * 3` + `quejas_t-1 * 1.5`).
    * `pct_cambio_saldo_ultimo_mes`: Tasa de variación del capital disponible en el último mes de actividad.

### 3. `features_scaled.csv`
* **Tipo de Contenido:** Dataset final preprocesado, listo para el consumo del algoritmo de gradiente.
* **Propiedades Estadísticas:** Todas las variables cuantitativas de `features_engineered.csv` han sido estandarizadas bajo el algoritmo Z-Score usando el estado guardado en `models/scaler_model.pkl`:
    $$z = \frac{x - \mu}{\sigma}$$
    Donde cada columna toma una distribución con $\mu = 0$ y $\sigma = 1$. Esto neutraliza la diferencia de magnitudes entre columnas (por ejemplo, saldos monetarios de seis cifras vs. variables binarias de $0/1$), asegurando que el optimizador de XGBoost no sufra sesgos de escala. La variable `target_fuga` permanece intacta de forma binaria.

---

## 🔁 Linealidad del Pipeline de Datos

El flujo de transformación de datos opera de manera estrictamente secuencial y síncrona a lo largo del proyecto:



[Generación Estocástica]
               ↓
        (src/data.py)
               ↓
  💾 data/banca_transacciones.csv  <-- (720k registros, formato largo)
               ↓
      (src/features.py)  <-- Regresiones lineales y pivoteo analítico
               ↓
  💾 data/features_engineered.csv <-- (120k registros, formato ancho)
               ↓
       (src/scaler.py)   <-- Ajuste Z-Score y persistencia (.pkl)
               ↓
  💾 data/features_scaled.csv     <-- Matriz lista para modelado (µ=0, σ=1)
               ↓
       (src/model.py)    <-- Entrenamiento de árboles XGBoost


       ---

## 🚨 Consideraciones de Consistencia en Producción

* **Inmutabilidad y Sincronización:** Las dimensiones de renglones e índices en `features_engineered.csv` y `features_scaled.csv` deben mantener correspondencia biunívoca exacta ($120,000$ registros indexados por el `id_cliente`).
* **Prevención de Data Drift:** Cualquier registro o vector nuevo simulado a través de la aplicación en caliente (`app.py`) no se añade directamente a estas matrices; en su lugar, se procesa de forma aislada utilizando los parámetros estadísticos fijos extraídos durante la creación de `features_scaled.csv` (preservados en el archivo `scaler_model.pkl`), garantizando la integridad de la inferencia matemática.