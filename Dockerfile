FROM python:3.13

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y netcat-openbsd && rm -rf /var/lib/apt/lists/*

# Crear carpeta de trabajo
WORKDIR /app

# Instalar dependencias de Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto del código
COPY . .

# Exponer el puerto de Django
EXPOSE 8000

# Comando para desarrollo
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
