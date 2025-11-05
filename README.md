# REST API приложение для управления организациями

## Описание
REST API для управления организациями, зданиями и видами деятельности с использованием FastAPI, SQLAlchemy и статической аутентификации по API ключу.


```

## Инструкция по разворачиванию

1. Убедитесь, что у вас установлен Docker и Docker Compose:
```bash
docker --version
docker-compose --version
```

2. Клонируйте/скопируйте все файлы проекта в одну директорию

3. Для корректной работы API необходимо создать файл .env в корне проекта.
Файл должен содержать ключевые параметры конфигурации, используемые приложением.

Пример:
# === API Key для аутентификации запросов ===
API_KEY=fastapi+pydantic+sqlalchemy+alembic

# === Конфигурация базы данных ===
# По умолчанию используется SQLite, база хранится локально в ./data/
DB_ENGINE=sqlite
DB_NAME=./data/organizations.db

# === Общие настройки Python ===
PYTHONUNBUFFERED=1


4. Запустите приложение:
```bash
docker-compose up --build -d
```

5. API будет доступен по адресу: http://localhost:8000

6. Документация Swagger UI: http://localhost:8000/docs

## API Endpoints

### Аутентификация
Все запросы требуют заголовок:
```
X-API-Key: (здесь API_KEY из .env)
```

### Организации
- `POST /organizations/` - Создать организацию
- `GET /organizations/` - Получить список организаций
- `GET /organizations/{id}` - Получить организацию по ID
- `DELETE /organizations/{id}` - Удалить организацию

### Здания
- `POST /organizations/{id}/buildings/` - Создать здание
- `GET /organizations/{id}/buildings/` - Получить здания организации

### Деятельности
- `POST /organizations/{id}/activities/` - Создать деятельность
- `GET /organizations/{id}/activities/` - Получить деятельности организации