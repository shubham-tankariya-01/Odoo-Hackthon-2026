import asyncio
import sys
import os

# Add backend directory to sys.path to run as script
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.database import AsyncSessionLocal
from app.models.user import User
from app.utils.constants import UserRole, UserStatus
from app.utils.security import hash_password
from sqlalchemy import select

async def create_admin():
    async with AsyncSessionLocal() as session:
        # Check if admin already exists
        result = await session.execute(select(User).where(User.email == "admin@assetflow.com"))
        admin = result.scalars().first()
        
        if admin:
            print("Admin user already exists.")
            return

        admin_user = User(
            name="System Admin",
            email="admin@assetflow.com",
            hashed_password=hash_password("admin123"),
            role=UserRole.ADMIN,
            status=UserStatus.ACTIVE
        )
        session.add(admin_user)
        await session.commit()
        print("Admin user created successfully! Email: admin@assetflow.com / Password: admin123")

if __name__ == "__main__":
    asyncio.run(create_admin())
