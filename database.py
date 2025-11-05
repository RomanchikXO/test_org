"""
Конфигурация подключения к базе данных
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

DB_ENGINE = os.getenv("DB_ENGINE", "sqlite")
DB_NAME = os.getenv("DB_NAME", "./data/organizations.db")

# SQLite база данных
SQLALCHEMY_DATABASE_URL = f"sqlite:///{DB_NAME}"

# Создание движка БД
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}  # Необходимо для SQLite
)

# Фабрика сессий
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    """
    Генератор сессии базы данных
    Используется как dependency в FastAPI эндпоинтах
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()