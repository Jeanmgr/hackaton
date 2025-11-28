#!/bin/bash
# Script para iniciar el servidor EcoLoop

# Ir al directorio del proyecto
cd "$(dirname "$0")"

echo "🚀 Iniciando EcoLoop Server..."
echo "📂 Directorio: $(pwd)"
echo ""

# Activar entorno virtual si existe
if [ -d "venv" ]; then
    echo "✓ Activando entorno virtual..."
    source venv/bin/activate
fi

# Instalar dependencias si es necesario
if [ ! -f ".dependencies_installed" ]; then
    echo "📦 Instalando dependencias..."
    pip install -r requirements.txt
    touch .dependencies_installed
fi

echo ""
echo "✅ Servidor listo en: http://localhost:8000"
echo "📖 Documentación API: http://localhost:8000/docs"
echo "👤 Usuarios: http://localhost:8000/usuarios"
echo "📍 Monitoreo: http://localhost:8000/monitoreo"
echo ""
echo "Presiona CTRL+C para detener el servidor"
echo ""

# Iniciar servidor
python -m uvicorn app:app --reload --host 0.0.0.0 --port 8000
