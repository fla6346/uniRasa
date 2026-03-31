FROM rasa/rasa:3.6.20-full

WORKDIR /app
COPY . .

USER root

RUN pip install requests
RUN rasa train --fixed-model-name modelo_uft

EXPOSE 5005

ENTRYPOINT []
CMD ["/bin/bash", "-c", "rasa run --enable-api --cors '*' --port 5005 --model models/modelo_uft.tar.gz --endpoints endpoints.yml & sleep 45 && python -m rasa_sdk.endpoint --actions actions --port 5055 & wait"]