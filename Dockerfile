# Dockerfile

# 1. BASE IMAGE: Usamos una imagen oficial de Python ligera.
FROM python:3.11-slim

# 2. WORKDIR: Establecemos el directorio de trabajo dentro del contenedor.
WORKDIR /app

# 3. COPY REQUIREMENTS: Copiamos el archivo de requisitos e instalamos las dependencias.
# Esto se hace primero para aprovechar el cache de Docker.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. COPY CODE: Copiamos el resto del código al directorio /app del contenedor.
# Esto incluye app.py, ssh_utils.py, config.ini, y la carpeta templates.
COPY . .

# 5. EXPOSE PORT: Indicamos a Docker que la aplicación usa el puerto 5000.
# Flask corre por defecto en 5000.
EXPOSE 5000

# 6. ENTRYPOINT/CMD: Definimos el comando que se ejecuta cuando el contenedor inicia.
# Aquí iniciamos la aplicación Flask.
CMD ["python", "app.py"]