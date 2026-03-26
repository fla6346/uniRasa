#!/bin/bash
# Inicia el action server en segundo plano
python -m rasa_sdk.endpoint --actions actions &

# Espera un poco para que el action server levante
sleep 5

# Inicia Rasa
rasa run --enable-api --cors "*" --port 5005