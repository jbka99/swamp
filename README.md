# Swamp 2.0

Форум на FastAPI с JWT авторизацией, PostgreSQL и Docker.

## Стек
- FastAPI, SQLAlchemy 2.0, Alembic, PostgreSQL, Docker

## Запуск локально

1. Клонировать репозиторий
2. Создать `.env` по примеру `.env.example`
3. Запустить:
```bash
docker compose up --build
docker compose exec app alembic upgrade head
```
4. Документация: `http://localhost:8000/docs`

## Функциональность
- Регистрация и авторизация (JWT)
- Категории, треды, комментарии
- Голосование за треды и комментарии
- Роли: superadmin, moderator, user
- Мягкое удаление с каскадом
- Поиск по тредам