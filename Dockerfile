# Используем базовый образ Python
FROM python:3.9-slim

# Устанавливаем переменную окружения PYTHONUNBUFFERED, чтобы вывод был направлен сразу на консоль без буферизации
ENV PYTHONUNBUFFERED 1

# Устанавливаем рабочую директорию в /redirect
WORKDIR /redirect

# Копируем файл requirements.txt в /redirect
COPY requirements.txt /redirect/

# Устанавливаем зависимости Python из файла requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Копируем содержимое текущего каталога в /redirect в образе
COPY . /redirect/

# Указываем Flask как приложение по умолчанию
ENV FLASK_APP app.py

# Запускаем сервер Flask при старте контейнера
CMD ["flask", "run", "--host=0.0.0.0"]
