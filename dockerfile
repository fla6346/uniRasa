# Dockerfile para Rasa en Render
FROM python:3.10-slim

# Instalar dependencias del sistema necesarias para compilar PyYAML
RUN apt-get update && apt-get install -y \
    build-essential \
    libyaml-dev \
    git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copiar primero requirements para aprovechar cache de Docker
COPY requirements.txt .

# Actualizar herramientas de build
RUN pip install --upgrade pip setuptools wheel

# Instalar PyYAML CON WHEEL precompilado PRIMERO
RUN pip install --no-cache-dir --only-binary=:all: PyYAML==6.0.1

# Luego instalar Rasa (aceptará PyYAML 6.0.1 aunque pida <6.0, funciona en práctica)
RUN pip install --no-cache-dir rasa==3.6.0 --ignore-installed PyYAML

# Copiar el resto del proyecto
COPY . .

# Entrenar el modelo (comenta esta línea si subes el modelo entrenado a GitHub)
RUN rasa train

# Variables de entorno
ENV PORT=5005
ENV PYTHONUNBUFFERED=1

# Exponer puerto
EXPOSE 5005

# Comando de inicio
CMD ["rasa", "run", "--enable-api", "--cors", "*", "--host", "0.0.0.0", "--port", "5005", "--model", "models"]