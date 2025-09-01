from app.database_folder.orm import AsyncOrm
import asyncio
from datetime import date


async def add_permissions():
    return await AsyncOrm.add_owner_permission(
        owner_permission_name="admin",
        owner_permission_description="admin"
    )


async def add_owner():
    return await AsyncOrm.add_owner(
        owner_firstname="admin",
        owner_surname="admin",
        owner_mail="admin@admin.com",
        owner_hashed_password="admin",
        owner_permission=1
    )


async def add_cat(owner_id, idx, gender):
    return await AsyncOrm.add_cat(
        cat_id=idx, 
        owner_id=owner_id, 
        cat_firstname=f"Barsik_{idx}", 
        cat_surname=f"Stalone{idx}",
        cat_gender=gender,
        cat_birthday=date(2020, 5, 17), 
        cat_microchip_number=f"{idx}",
        cat_EMS_colour="black",
        cat_litter="123213"
    )


async def main_add_workflow():
    try:
        await add_permissions()
        await add_owner()
        await add_owner()
        await add_cat(1, 2, "Male")
        await add_cat(2, 4, "Female")
        print("✅ Database initialization completed successfully!")
    except Exception as e:
        print(f"❌ Error during database initialization: {e}")
        raise


def start_add_workflow():
    asyncio.run(main_add_workflow())
