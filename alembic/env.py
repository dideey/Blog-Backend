import asyncio
import os
from logging.config import fileConfig

from alembic import context
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.pool import NullPool
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import your Base metadata
from models import Base

# Alembic Config object
config = context.config

# Set target metadata for 'autogenerate'
target_metadata = Base.metadata

# Get database URL from environment
DATABASE_URL = os.getenv("DATABASE_URL", "").strip()
print(f"DATABASE_URL: '{DATABASE_URL}'")  

if DATABASE_URL is None:
    raise ValueError("DATABASE_URL environment variable not set!")

# Override sqlalchemy.url in config
config.set_main_option("sqlalchemy.url", DATABASE_URL)

def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    context.configure(
        url=DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def do_run_migrations(connection):
    context.configure(connection=connection, target_metadata=target_metadata)
    with context.begin_transaction():
        context.run_migrations()

async def run_migrations_online():
    """Run migrations in 'online' mode."""
    connectable = create_async_engine(
        DATABASE_URL,
        poolclass=NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())
