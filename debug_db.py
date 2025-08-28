#!/usr/bin/env python3
"""
Debug script to identify database connection issues
"""

import asyncio
import os
from app.database_folder.db_setting import settings
from app.database_folder.postgres import check_db_connection, async_session
from app.database_folder.orm import AsyncOrm


async def test_database_connection():
    """Test database connection and basic operations"""
    print("🔍 Testing database connection...")
    
    # Check environment variables
    print("📋 Environment variables:")
    print(f"   DB_HOST: {settings.DB_HOST}")
    print(f"   DB_PORT: {settings.DB_PORT}")
    print(f"   DB_USER: {settings.DB_USER}")
    print(f"   DB_NAME: {settings.DB_NAME}")
    print(f"   DB_PASS: {'*' * len(settings.DB_PASS) if settings.DB_PASS else 'NOT SET'}")
    
    # Test sync connection
    print("\n🔗 Testing synchronous connection...")
    try:
        if check_db_connection():
            print("✅ Synchronous connection successful!")
        else:
            print("❌ Synchronous connection failed!")
            return False
    except Exception as e:
        print(f"❌ Synchronous connection error: {e}")
        return False
    
    # Test async connection
    print("\n🔄 Testing asynchronous connection...")
    try:
        async with async_session() as session:
            await session.execute("SELECT 1")
            print("✅ Asynchronous connection successful!")
    except Exception as e:
        print(f"❌ Asynchronous connection error: {e}")
        return False
    
    # Test basic ORM operation
    print("\n🐱 Testing ORM operations...")
    try:
        count, owners = await AsyncOrm.get_owner()
        print(f"✅ ORM operation successful! Found {count} owners")
    except Exception as e:
        print(f"❌ ORM operation error: {e}")
        return False
    
    print("\n🎉 All database tests passed!")
    return True


def main():
    """Main function to run the debug tests"""
    print("🚀 Starting database debug tests...")
    
    # Check if .env file exists
    if not os.path.exists('.env'):
        print("❌ .env file not found!")
        print("📝 Please create a .env file with the following variables:")
        print("   DB_HOST=localhost")
        print("   DB_PORT=5432")
        print("   DB_USER=your_username")
        print("   DB_PASS=your_password")
        print("   DB_NAME=cat_database")
        return
    
    # Run async tests
    try:
        result = asyncio.run(test_database_connection())
        if result:
            print("\n✅ Database is ready for use!")
        else:
            print("\n❌ Database has issues that need to be resolved.")
    except Exception as e:
        print(f"\n💥 Unexpected error: {e}")


if __name__ == "__main__":
    main()
