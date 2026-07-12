import asyncio
import sys
import os
from sqlalchemy import text

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app.database import engine

async def check_connection():
    print("Testing PostgreSQL connection...")
    try:
        async with engine.connect() as conn:
            # Test simple query
            result = await conn.execute(text("SELECT version();"))
            version = result.scalar()
            print(f"Success! Connected to database!\nDatabase Version: {version}")
            
            # Test fetching users
            print("\nFetching users from database...")
            users = await conn.execute(text("SELECT id, name, email, role, status FROM users;"))
            user_rows = users.fetchall()
            
            if not user_rows:
                print("No users found in the database.")
            else:
                for user in user_rows:
                    print(f"- User: {user.name} ({user.email}) | Role: {user.role} | Status: {user.status} | ID: {user.id}")
                    
    except Exception as e:
        print(f"Database connection failed: {e}")

if __name__ == "__main__":
    asyncio.run(check_connection())
