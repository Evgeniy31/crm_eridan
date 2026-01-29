# Use the official Python image from the Docker Hub (Используйте официальный образ Python из Docker Hub)
FROM python:3.11-slim

# Set environment variables (Установите переменные среды)
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory (Установите рабочий каталог)
WORKDIR /app

# Install system dependencies (Установка системных зависимостей)
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies (Скопируйте требования и установите зависимости Python)
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the project files (Скопируйте файлы проекта)
COPY . /app/

# Collect static files (Сбор статических файлов)
RUN python manage.py collectstatic --noinput

# Run migrations (Запуск миграций)
RUN python manage.py migrate

# Expose the port the app runs on (Укажите порт, на котором работает приложение)
EXPOSE 8000

# Run the application (Запустите приложение)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
