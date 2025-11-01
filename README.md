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

3. Запустите приложение:
```bash
docker-compose up --build -d
```

4. API будет доступен по адресу: http://localhost:8000

5. Документация Swagger UI: http://localhost:8000/docs

## API Endpoints

### Аутентификация
Все запросы требуют заголовок:
```
X-API-Key: fastapi+pydantic+sqlalchemy+alembic
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