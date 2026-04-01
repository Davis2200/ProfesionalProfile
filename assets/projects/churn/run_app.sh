#!/bin/bash

# Script para ejecutar la aplicación Streamlit correctamente

# Cambiar al directorio del proyecto
cd "$(dirname "$0")"

echo "📁 Directorio actual: $(pwd)"
echo "🔍 Buscando entorno virtual..."

# Activar el entorno virtual
if [ -d "venv" ]; then
    source venv/bin/activate
    echo "✅ Entorno virtual activado"
    echo "🐍 Python: $(which python)"
else
    echo "❌ ERROR: El directorio 'venv' no existe"
    echo "👉 Por favor ejecuta primero: python3 -m venv venv"
    exit 1
fi

# Verificar que xgboost está disponible
python -c "import xgboost; print('✅ xgboost disponible')" || {
    echo "⚠️  Instalando xgboost..."
    pip install xgboost
}

echo ""
echo "🚀 Iniciando Streamlit en puerto 8501..."
echo "📱 Abre tu navegador en: http://localhost:8501"
echo ""

# Ejecutar Streamlit
streamlit run app.py --logger.level=error
