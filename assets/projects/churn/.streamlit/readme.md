# 🎨 Configuración de Entorno de Despliegue (`/.streamlit`)

Este directorio contiene los archivos de configuración técnica para **Streamlit**, el framework web utilizado para desplegar el *Live Risk Simulator* en entornos locales y de producción. A través de estos parámetros, se controla tanto el comportamiento del servidor de sockets como la paleta de diseño de la interfaz de usuario.

---

## 🗃️ Arquitectura de Configuración

El archivo principal de este directorio es `config.toml`, el cual está segmentado en tres bloques clave de infraestructura y diseño:

### 1. Tematización Visual (`[theme]`)
Define la identidad visual de la plataforma predictiva para garantizar una experiencia limpia y profesional:
* `primaryColor = "#1f77b4"`: Tono azul institucional para resaltar componentes interactivos como botones de ejecución de inferencia, selectores y métricas destacadas.
* `backgroundColor = "#ffffff"`: Fondo principal claro que maximiza la legibilidad de las tablas de datos y gráficos de importancia de variables.
* `secondaryBackgroundColor = "#f0f2f6"`: Gris tenue estructural para segmentar barras laterales (*sidebars*) y contenedores de formularios de datos del cliente.
* `textColor = "#262730"`: Contraste oscuro de alta visibilidad para textos informativos y reportes matemáticos.
* `font = "sans serif"`: Tipografía limpia y moderna orientada a la lectura fluida de tableros analíticos.

### 2. Parámetros del Cliente Web (`[client]`)
* `showErrorDetails = true`: Permite la visualización detallada de excepciones en la interfaz web durante la fase de desarrollo, facilitando la depuración rápida si ocurre una falla en la carga de los artefactos (`.pkl` o `.json`).
* `toolbarMode = "viewer"`: Optimiza la interfaz eliminando las opciones de edición para el usuario final, presentando una aplicación limpia enfocada estrictamente en la consulta del dashboard.

### 3. Configuración del Servidor (`[server]`)
Controla la exposición de red y la automatización del backend:
* `port = 8501`: Puerto de red por defecto para la escucha de peticiones HTTP del simulador.
* `headless = true`: Desactiva el auto-arranque del navegador local al ejecutar el comando. Esto es mandatorio para despliegues en servidores en la nube (como Streamlit Community Cloud o instancias Docker) donde no se cuenta con un entorno gráfico activo.
* `runOnSave = true`: Característica de hot-reload. El servidor web monitorea activamente cambios en el backend (`app.py`), actualizando automáticamente la interfaz en producción sin necesidad de reiniciar manualmente el proceso en la terminal.

---

## 🛠️ Modos de Uso Asociados

Esta configuración se inyecta de forma transparente al arrancar la aplicación nativa. Si necesitas anular temporalmente alguna protección de red (como XSRF o CORS) en ambientes controlados de desarrollo, se puede invocar de la siguiente manera:

```bash
streamlit run app.py --server.enableCORS false --server.enableXsrfProtection false