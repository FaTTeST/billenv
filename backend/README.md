# PostSocial Backend

Backend API для сервиса PostSocial на FastAPI.

## Требования

- Python 3.12+
- PostgreSQL 18.3
- Redis

## Установка

```bash
# Создание виртуального окружения
python -m venv venv
source venv/bin/activate  # Linux/Mac
# или
venv\Scripts\activate  # Windows

# Установка зависимостей
pip install -r requirements.txt

# Копирование .env.example в .env и настройка переменных
cp .env.example .env
```

## Запуск

```bash
# Запуск сервера разработки
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Документация API доступна по адресу http://localhost:8000/docs
```

## Структура проекта

```
backend/
├── app/
│   ├── api/          # API роутеры
│   ├── core/         # Конфигурация, безопасность
│   ├── db/           # Подключение к БД
│   ├── models/       # SQLAlchemy модели
│   ├── schemas/      # Pydantic схемы
│   ├── services/     # Бизнес-логика
│   ├── tasks/        # Celery задачи
│   └── main.py       # Точка входа
├── tests/            # Тесты
├── requirements.txt  # Зависимости
└── .env.example      # Пример переменных окружения
```

## API Endpoints

- `POST /api/v1/auth/register` - Регистрация пользователя
- `POST /api/v1/auth/login` - Вход (получение токена)
- `GET /api/v1/auth/me` - Текущий пользователь
- `GET /api/v1/plans/` - Список тарифов
- `POST /api/v1/subscriptions/` - Создание подписки
- `GET /api/v1/sources/` - Источники контента
- `GET /api/v1/recipients/` - Получатели
- `GET /api/v1/posts/` - Посты
- `GET /api/v1/mailings/` - Рассылки
- `GET /api/v1/payments/` - Платежи

## Разработка

```bash
# Запуск тестов
pytest

# Форматирование кода
black app/
isort app/

# Проверка типов
mypy app/
```
