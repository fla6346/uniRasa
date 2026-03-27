#!/bin/bash
set -e  # Salir si algún comando falla

echo "🚀 Iniciando Action Server en puerto 5055..."
# Iniciar Action Server en background en puerto 5055 (interno)
python -m rasa_sdk.endpoint --actions actions --port 5055 --hostname localhost &
ACTION_PID=$!

# Esperar que el action server esté listo
echo "⏳ Esperando que el Action Server esté listo..."
sleep 8

# Verificar que el action server está corriendo
if ! kill -0 $ACTION_PID 2>/dev/null; then
  echo "❌ Error: El Action Server no pudo iniciarse"
  exit 1
fi

echo "✅ Action Server listo. Iniciando Rasa Core..."

# Iniciar Rasa Core en el puerto que Render asigna ($PORT)
# Especificar el modelo entrenado
exec rasa run \
  --enable-api \
  --cors "*" \
  --port $PORT \
  --model models/modelo_uft.tar.gz \
  --endpoints endpoints.yml \
  --credentials credentials.yml