FROM rasa/rasa:3.6.20-full

WORKDIR /app
COPY . .

USER root

# Instalar supervisord y dependencias
RUN apt-get update && apt-get install -y supervisor && rm -rf /var/lib/apt/lists/*
RUN pip install requests

# Entrenar el modelo
RUN rasa train --fixed-model-name modelo_uft

# Crear directorio para logs de supervisord
RUN mkdir -p /var/log/supervisor

# Copiar configuración de supervisord
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

EXPOSE 5005
ENV PORT=5005

# Iniciar supervisord (NO usar CMD array, usar shell form)
CMD /usr/bin/supervisord -c /etc/supervisor/conf.d/supervisord.conf