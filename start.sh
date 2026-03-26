#!/bin/bash
# Inicia el action server en segundo plano
python -m rasa_sdk.endpoint --actions actions &

# Espera que levante
sleep 5

# Inicia Rasa apuntando al action server
rasa run --enable-api --cors "*" --port 5005
