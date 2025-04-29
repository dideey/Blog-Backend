from database import DATABASE_URL, engine
import asyncio

async def test():
    print(f"Final URL: {repr(DATABASE_URL)}")
    try:
        async with engine.connect() as conn:
            print("✅ Connection successful!")
    except Exception as e:
        print(f"❌ Connection failed: {repr(e)}")

asyncio.run(test())