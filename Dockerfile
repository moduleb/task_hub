FROM python:3.13.0rc1-slim

# Копируем файлы poetry в контейнер
WORKDIR /app
COPY requirements.txt ./

# Устанавливаем  зависимости
RUN pip install -r requirements.txt

# Копируем остальные файлы проекта в контейнер
COPY . .

# Устанавливаем переменную окружения для загрузки конфигурации production
ENV FASTAPI_ENV=production

# Запуск приложения
CMD python run.py
