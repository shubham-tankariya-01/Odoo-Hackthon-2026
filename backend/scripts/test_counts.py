import asyncio
import os
import sys

from sqlalchemy import text

# Allow imports from the app package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.database import engine


TABLES = [
    "users",
    "departments",
    "asset_categories",
    "assets",
    "asset_allocations",
    "resource_bookings",
    "maintenance_requests",
    "audit_cycles",
    "audit_findings",
    "activity_logs",
]


async def table_exists(conn, table_name: str) -> bool:
    result = await conn.execute(
        text(
            """
            SELECT EXISTS (
                SELECT 1
                FROM information_schema.tables
                WHERE table_schema = 'public'
                AND table_name = :table_name
            );
            """
        ),
        {"table_name": table_name},
    )
    return result.scalar()


async def count_rows(conn, table_name: str) -> int:
    result = await conn.execute(text(f"SELECT COUNT(*) FROM {table_name};"))
    return result.scalar()


async def main():
    print("=" * 50)
    print("AssetFlow Database Health Check")
    print("=" * 50)

    try:
        async with engine.connect() as conn:
            print("\nDatabase connected successfully!\n")

            for table in TABLES:
                exists = await table_exists(conn, table)

                if not exists:
                    print(f"[FAIL] {table:<25} DOES NOT EXIST")
                    continue

                count = await count_rows(conn, table)
                print(f"[OK]   {table:<25} {count:>5} row(s)")

    except Exception as e:
        print(f"\nDatabase Error: {e}")

    print("\nDone.")


if __name__ == "__main__":
    asyncio.run(main())