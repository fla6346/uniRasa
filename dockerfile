FROM rasa/rasa:3.6.20-full

WORKDIR /app
COPY . .

USER root

# Solo instala requests para el action server
RUN pip install requests

# Entrena el modelo
RUN rasa train --fixed-model-name modelo_uft

EXPOSE 5005
EXPOSE 5055

COPY start.sh /app/start.sh
RUN chmod +x /app/start.sh

USER 1001
CMD ["/app/start.sh"]