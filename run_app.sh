#!/bin/bash
# 🚀 Script para ejecutar la interfaz Streamlit

set -e

echo "════════════════════════════════════════════════════════════"
echo "  🏥 Sistema de Automatización Médica - Interfaz Desktop"
echo "════════════════════════════════════════════════════════════"
echo ""

# Verificar Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 no está instalado"
    exit 1
fi

echo "✅ Python encontrado: $(python3 --version)"
echo ""

# Crear venv si no existe
if [ ! -d "venv" ]; then
    echo "📦 Creando virtual environment..."
    python3 -m venv venv
fi

# Activar venv
echo "🔌 Activando virtual environment..."
source venv/bin/activate

# Instalar dependencias
echo "📥 Instalando dependencias..."
pip install -r requirements.txt > /dev/null 2>&1

echo ""
echo "════════════════════════════════════════════════════════════"
echo "  ✨ Iniciando aplicación..."
echo "════════════════════════════════════════════════════════════"
echo ""
echo "🌐 La interfaz se abrirá automáticamente en tu navegador"
echo "📍 URL: http://localhost:8501"
echo ""
echo "💡 Controles:"
echo "   • Press Ctrl+C para detener"
echo "   • Press 'r' para recargar"
echo "   • Press 'c' para limpiar cache"
echo ""
echo "════════════════════════════════════════════════════════════"
echo ""

# Ejecutar Streamlit
streamlit run app.py
