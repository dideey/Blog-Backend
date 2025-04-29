from database import DATABASE_URL, engine
import asyncio

async def test_connection():
    try:
        async with engine.connect() as conn:
            print("✅ Connection successful!")
            print(f"Using URL: {DATABASE_URL}")
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        print(f"Problem URL: {repr(DATABASE_URL)}")  # Shows hidden characters

asyncio.run(test_connection())