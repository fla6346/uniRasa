#!/bin/bash
set -e

# Limitar memoria de Python
export PYTHONMALLOC=malloc
export MALLOC_ARENA_MAX=2

echo "🚀 Iniciando Action Server..."
# Iniciar Action Server con menos workers
python -m rasa_sdk.endpoint --actions actions --port 5055 &
ACTION_PID=$!

sleep 8

if ! kill -0 $ACTION_PID 2>/dev/null; then
  echo "❌ Error: Action Server no pudo iniciarse"
  exit 1
fi

echo "✅ Action Server listo. Iniciando Rasa Core..."

# Iniciar Rasa Core con configuración optimizada
exec rasa run \
  --enable-api \
  --cors "*" \
  --port $PORT \
  --model models/modelo_uft.tar.gz \
  --endpoints endpoints.yml \
  --credentials credentials.yml \
  --log-level warning  # ← Menos logging = menos memoria