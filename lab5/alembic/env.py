import os
from logging.config import fileConfig
from sqlalchemy import create_engine, pool
from alembic import context
from dotenv import load_dotenv

# Загружаем переменные из .env
load_dotenv()

# Конфигурация Alembic
config = context.config
if config.config_file_name:
    fileConfig(config.config_file_name)

from app.db.base import Base
from app.models.user import User
from app.models.corpus import Corpus  # Добавь сюда остальные модели

target_metadata = Base.metadata

DB_URL = os.getenv("DB_URL", "sqlite:///app/db/database.db")


def run_migrations_offline():
    """Запуск миграций в оффлайн-режиме (без подключения к БД)"""
    context.configure(
        url=DB_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Запуск миграций в онлайн-режиме (с подключением к БД)"""
    connectable = create_engine(DB_URL, echo=True, poolclass=pool.NullPool)
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()

