# REST API приложение для управления организациями

## Описание
REST API для управления организациями, зданиями и видами деятельности с использованием FastAPI, SQLAlchemy 
и статической аутентификации по API ключу.

Так как проект тестовый то была выбрана sqlite как легковесная бд-шка )) для продакшена можно было бы юзать PostgreSQL

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

5. Настройка alembic
```bash
docker-compose exec api alembic init alembic
```
После этого откройте alembic.ini и укажите URL вашей базы данных:
sqlalchemy.url = sqlite:///./data/organizations.db

Создаём первую миграцию и применяем её:
```bash
docker-compose exec api alembic revision --autogenerate -m "Initial migration"
docker-compose exec api alembic upgrade head
```

6. API будет доступен по адресу: http://localhost:8000

7. Документация Swagger UI: http://localhost:8000/docs

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