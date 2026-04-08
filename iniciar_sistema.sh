#!/bin/bash
echo "=========================================="
echo "    INICIANDO SISTEMA DE ANALITICA"
echo "=========================================="
echo ""

echo "[1/2] Iniciando el motor de IA..."
# En Linux se usa 'source' y la carpeta 'bin' en lugar de 'Scripts'
# El '&' al final hace que el proceso corra en segundo plano sin bloquear la terminal
source venv/bin/activate && python3 index.py &

echo "[2/2] Levantando el Panel de Control..."
source venv/bin/activate && python3 -m streamlit run dashboard.py &

echo ""
echo "¡Sistema iniciado con éxito en segundo plano!"