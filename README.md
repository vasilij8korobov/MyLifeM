# MyLifeM - Личный дневник

Веб-приложение для ведения персонального дневника с возможностью создания, редактирования и поиска записей.

## 🌟 Особенности

- 📝 Создание записей с тегами и прикреплением файлов
- 🔐 Приватные/публичные записи
- 🔍 Поиск по содержимому
- 📱 Адаптивный интерфейс (Bootstrap 5)
- 🐳 Готовые Docker-конфигурации

## 🛠 Технологии

- **Backend**: Django 4.2, Python 3.11
- **Frontend**: Bootstrap 5, jQuery (опционально)
- **База данных**: PostgreSQL
- **Инфраструктура**: Docker, Gunicorn, Nginx

## 🚀 Быстрый старт

### 1. Требования
- Docker 20.10+
- Docker Compose 2.0+

### 2. Запуск в development-режиме

# Клонировать репозиторий
git clone https://github.com/vasilij8korobov/MyLifeM.git
cd MyLifeM

# Запустить сервисы
docker-compose -f docker-compose.yml up --build
Приложение будет доступно по адресу: http://localhost:8000
Админ-панель: http://localhost:8000/admin

📂 Структура проекта

MyLifeM/
├── config/              # Настройки Django
├── diary/               # Приложение дневника
│   ├── models.py        # Модели DiaryEntry, Tag
│   ├── views.py         # Логика работы с записями
│   └── templates/       # Шаблоны HTML
├── users/               # Пользовательская система
├── static/              # CSS/JS/Изображения
├── .env.example         # Шаблон переменных окружения
├── docker-compose.yml   # Конфигурация Docker
└── README.md            # Этот файл

🔧 Настройка окружения
1. Создайте .env файл на основе .env.example:
cp .env.example .env

2. Заполните обязательные переменные на примере .env.example:
SECRET_KEY=

DEBUG=

NAME=
USER=
PASSWORD=
HOST=
PORT=

DATABASE_URL=
ALLOWED_HOSTS=

🧪 Тестирование
docker-compose exec web python manage.py test

Соберите статику:
docker-compose exec web python manage.py collectstatic --noinput


# Инструкция для разработки без Docker:
## 🖥 Локальная установка (без Docker)

1. Установите PostgreSQL и создайте БД
2. Создайте виртуальное окружение:
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
3. 
Установите зависимости:
pip install -r requirements.txt

Установите зависимости разработчика(опционально):
pip install -r requirements-dev.txt


Примените миграции:
python manage.py migrate

Запуск приложения:
python manage.py runserver
