# PostSocial Backend

Backend API для сервиса PostSocial на FastAPI.

## Структура проекта

```
backend/
├── app/
│   ├── api/          # API роуты
│   ├── core/         # Конфигурация, безопасность
│   ├── db/           # База данных, сессии
│   ├── models/       # SQLAlchemy модели
│   ├── schemas/      # Pydantic схемы
│   ├── services/     # Бизнес-логика, интеграции
│   └── utils/        # Утилиты
├── tests/            # Тесты
├── requirements.txt  # Зависимости
└── main.py          # Точка входа
```

## Установка

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
```

## Запуск

```bash
uvicorn app.main:app --reload
```

## Технологический стек

- Python 3.12+
- FastAPI
- SQLAlchemy 2.0
- PostgreSQL 18.3
- Celery + Redis
- Pydantic
