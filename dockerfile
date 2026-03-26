FROM rasa/rasa:3.6.20-full

WORKDIR /app
COPY . .

USER root

# Instala dependencias del action server
RUN pip install rasa-sdk requests

# Entrena el modelo
RUN rasa train --fixed-model-name modelo_uft

EXPOSE 5005
EXPOSE 5055

# Script de inicio que lanza ambos procesos
COPY start.sh /app/start.sh
RUN chmod +x /app/start.sh

USER 1001
CMD ["/app/start.sh"]