# Guía de Ejecución - App Streamlit de Análisis de Riesgo de Clientes

## Requisitos Previos
- Python 3.8 o superior
- pip3

## Instalación Local (Primera vez)

### 1. Crear entorno virtual (ya está creado)
```bash
cd /workspaces/ProfesionalProfile/assets/projects/churn
python3 -m venv venv
```

### 2. Activar el entorno virtual

**En Linux/Mac:**
```bash
source venv/bin/activate
```

**En Windows:**
```bash
venv\Scripts\activate
```

### 3. Instalar dependencias
```bash
pip install -r requierements.txt
```

## Ejecución de la App

### Opción 1: Usar el script (Recomendado)
```bash
./run_app.sh
```

### Opción 2: Ejecutar manualmente
```bash
# 1. Activar entorno virtual
source venv/bin/activate

# 2. Ejecutar streamlit
streamlit run app.py
```

## Acceso en el navegador
La aplicación estará disponible en: **http://localhost:8501**

## Para detener la aplicación
Presiona `Ctrl + C` en la terminal

## Solución de Problemas

### Si xgboost no se instala correctamente:
```bash
pip install --upgrade pip setuptools wheel
pip install xgboost>=2.0.0
```

### Si hay problemas de rutas:
Asegúrate de que los siguientes archivos existan:
- `models/modelo_fuga_final.json` ✓
- `scaler_model.pkl` ✓

### Para verificar que todo está instalado:
```bash
pip list | grep -E 'streamlit|xgboost|pandas|scikit-learn'
```

## Configuración para GitHub

Los archivos principales que GitHub necesita:
1. `requierements.txt` - Dependencias con versiones específicas ✓
2. `.streamlit/config.toml` - Configuración de Streamlit ✓
3. `app.py` - Aplicación actualizada con rutas absolutas ✓
4. `venv/` - NO incluir en repositorio (agregar a .gitignore)

### Crear .gitignore (si no existe):
```
venv/
__pycache__/
*.pyc
.pytest_cache/
.streamlit/secrets.toml
.DS_Store
```

## Variables de entorno (opcional para GitHub)
Si usas Streamlit Cloud (streamlit.io), puedes configurar en `secrets.toml`:
```toml
# .streamlit/secrets.toml (NO en Git)
api_key = "tu_clave_aqui"
```
