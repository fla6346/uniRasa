FROM rasa/rasa:3.6.20-full

WORKDIR /app
COPY . .

USER root

# DEBUG: lista los archivos para verificar que domain.yml existe
RUN ls -la && cat domain.yml

RUN pip install requests
RUN rasa train --fixed-model-name modelo_uft

EXPOSE 5005
EXPOSE 5055

COPY start.sh /app/start.sh
RUN chmod +x /app/start.sh

USER 1001
CMD ["/app/start.sh"]