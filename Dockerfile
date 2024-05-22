# imagen Python para el backend
FROM python:3.9 AS backend

# directorio backend
WORKDIR /app/backend

# Copiar las dependencias al directorio del contenedor
COPY ./backend/requirements.txt .

# instalar las dependencias en el contenedor
RUN pip install --no-cache-dir -r requirements.txt

# Copia código fuente del backend
COPY ./backend/ .

#poner en escucha el puerto 5000 para el backend
EXPOSE 5000

# Comando para ejecutar backend
CMD ["python", "App_IntContinua.py"]