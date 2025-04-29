import os
import re
import ssl
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from typing import AsyncGenerator
from dotenv import load_dotenv

load_dotenv()

def nuclear_clean_url(url: str) -> str:
    """Aggressively clean and validate the database URL"""
    if not url:
        raise ValueError("DATABASE_URL is not set")
    
    # 1. Remove ALL whitespace (including invisible unicode spaces)
    url = re.sub(r'\s+', '', url)
    
    # 2. Remove all quotes
    url = url.replace('"', '').replace("'", "")
    
    # 3. Verify the URL structure with a more flexible regex
    if not re.match(r'^postgresql\+asyncpg://[a-zA-Z0-9_]+:.+@[a-zA-Z0-9\-\.]+/[a-zA-Z0-9_]+(\?.*)?$', url):
        raise ValueError(f"Invalid database URL structure: {repr(url)}")
    
    return url

# Get and clean the URL
raw_url = os.getenv("DATABASE_URL")
DATABASE_URL = nuclear_clean_url(raw_url)

# Configure SSL context
ssl_context = ssl.create_default_context()
ssl_context.check_hostname = True
ssl_context.verify_mode = ssl.CERT_REQUIRED

# Create async engine
engine = create_async_engine(
    DATABASE_URL,
    echo=True,
    pool_pre_ping=True,
    connect_args={
        "ssl": ssl_context  # Pass SSL context here
    }
)

# Create session maker
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Dependency
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session