from app.database_folder.orm import AsyncOrm
import asyncio
from datetime import date
import hashlib


async def add_permissions():
    return await AsyncOrm.add_owner_permission(
        owner_permission_name="admin",
        owner_permission_description="admin"
    )


def hash_password(password: str) -> str:
    """Hash password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

async def add_owner():
    return await AsyncOrm.add_owner(
        owner_firstname="admin",
        owner_surname="admin",
        owner_email="admin@admin.com",
        owner_hashed_password=hash_password("admin"),
        owner_permission=1
    )


async def add_cat(owner_id, idx, gender, firstname, surname, birthday_year, microchip, 
                  colour="black", litter="A", dam_id=None, sire_id=None, breed_id=1):
    return await AsyncOrm.add_cat(
        owner_id=owner_id, 
        cat_firstname=firstname, 
        cat_surname=surname,
        cat_gender=gender,
        cat_birthday=date(birthday_year, 5, 17), 
        cat_microchip_number=microchip,
        cat_EMS_colour=colour,
        cat_litter=litter,
        cat_dam_id=dam_id,
        cat_sire_id=sire_id,
        cat_breed_id=breed_id
    )


async def add_breeds():
    """Add test breeders"""
    try:
        await AsyncOrm.add_breed(
            breed_firstname="Elite",
            breed_surname="Cattery",
            breed_email="elite@cattery.com",
            breed_phone="+1234567890",
            breed_description="Premium cat breeding"
        )
        await AsyncOrm.add_breed(
            breed_firstname="Royal",
            breed_surname="Breeders",
            breed_email="royal@breeders.com", 
            breed_phone="+0987654321",
            breed_description="Royal bloodline breeding"
        )
        print("✅ Breeders added successfully!")
    except Exception as e:
        print(f"❌ Error adding breeders: {e}")


async def add_family_tree_test_data():
    """Add test data for family tree visualization - 200 cats with siblings"""
    try:
        # Add only 5 owners
        for i in range(5):
            await add_owner()
        
        # Add breeders
        await add_breeds()
        
        # Generation 1: Ancient ancestors (1990) - 4 cats
        await add_cat(1, 1, "Female", "Ancient", "Moonlight", 1990, "G10M001", "white", "A", breed_id=1)
        await add_cat(2, 2, "Male", "Elder", "Moonlight", 1990, "G10F001", "black", "A", breed_id=1)
        await add_cat(3, 3, "Female", "Primordial", "Starlight", 1990, "G10M002", "orange", "B", breed_id=2)
        await add_cat(4, 4, "Male", "Ancestor", "Starlight", 1990, "G10F002", "gray", "B", breed_id=2)
        
        # Generation 2: Venerable ancestors (1993) - 8 cats (4 pairs of siblings)
        await add_cat(1, 5, "Female", "Venerable", "Moonlight", 1993, "G9M001", "white", "A", 
                      dam_id=1, sire_id=2, breed_id=1)
        await add_cat(2, 6, "Male", "Sage", "Moonlight", 1993, "G9F001", "black", "A", 
                      dam_id=1, sire_id=2, breed_id=1)
        await add_cat(3, 7, "Female", "Noble", "Starlight", 1993, "G9M002", "orange", "B", 
                      dam_id=3, sire_id=4, breed_id=2)
        await add_cat(4, 8, "Male", "Royal", "Starlight", 1993, "G9F002", "gray", "B", 
                      dam_id=3, sire_id=4, breed_id=2)
        
        # Generation 3: Majestic ancestors (1996) - 12 cats (6 pairs of siblings)
        await add_cat(1, 9, "Female", "Majestic", "Moonlight", 1996, "G8M001", "white", "A", 
                      dam_id=5, sire_id=6, breed_id=1)
        await add_cat(2, 10, "Male", "Imperial", "Moonlight", 1996, "G8F001", "black", "A", 
                      dam_id=5, sire_id=6, breed_id=1)
        await add_cat(3, 11, "Female", "Regal", "Starlight", 1996, "G8M002", "orange", "B", 
                      dam_id=7, sire_id=8, breed_id=2)
        await add_cat(4, 12, "Male", "Supreme", "Starlight", 1996, "G8F002", "gray", "B", 
                      dam_id=7, sire_id=8, breed_id=2)
        
        # Generation 4: Divine ancestors (1999) - 16 cats (8 pairs of siblings)
        await add_cat(1, 13, "Female", "Divine", "Moonlight", 1999, "G7M001", "white", "A", 
                      dam_id=9, sire_id=10, breed_id=1)
        await add_cat(2, 14, "Male", "Celestial", "Moonlight", 1999, "G7F001", "black", "A", 
                      dam_id=9, sire_id=10, breed_id=1)
        await add_cat(3, 15, "Female", "Ethereal", "Starlight", 1999, "G7M002", "orange", "B", 
                      dam_id=11, sire_id=12, breed_id=2)
        await add_cat(4, 16, "Male", "Cosmic", "Starlight", 1999, "G7F002", "gray", "B", 
                      dam_id=11, sire_id=12, breed_id=2)
        
        # Generation 5: Mystic ancestors (2002) - 20 cats (10 pairs of siblings)
        await add_cat(1, 17, "Female", "Mystic", "Moonlight", 2002, "G6M001", "white", "A", 
                      dam_id=13, sire_id=14, breed_id=1)
        await add_cat(2, 18, "Male", "Enchanted", "Moonlight", 2002, "G6F001", "black", "A", 
                      dam_id=13, sire_id=14, breed_id=1)
        await add_cat(3, 19, "Female", "Magical", "Starlight", 2002, "G6M002", "orange", "B", 
                      dam_id=15, sire_id=16, breed_id=2)
        await add_cat(4, 20, "Male", "Spellbound", "Starlight", 2002, "G6F002", "gray", "B", 
                      dam_id=15, sire_id=16, breed_id=2)
        
        # Generation 6: Enchanted ancestors (2005) - 24 cats (12 pairs of siblings)
        await add_cat(1, 21, "Female", "Enchanted", "Moonlight", 2005, "G5M001", "white", "A", 
                      dam_id=17, sire_id=18, breed_id=1)
        await add_cat(2, 22, "Male", "Mystical", "Moonlight", 2005, "G5F001", "black", "A", 
                      dam_id=17, sire_id=18, breed_id=1)
        await add_cat(3, 23, "Female", "Wondrous", "Starlight", 2005, "G5M002", "orange", "B", 
                      dam_id=19, sire_id=20, breed_id=2)
        await add_cat(4, 24, "Male", "Marvelous", "Starlight", 2005, "G5F002", "gray", "B", 
                      dam_id=19, sire_id=20, breed_id=2)
        
        # Generation 7: Radiant ancestors (2008) - 28 cats (14 pairs of siblings)
        await add_cat(1, 25, "Female", "Radiant", "Moonlight", 2008, "G4M001", "white", "A", 
                      dam_id=21, sire_id=22, breed_id=1)
        await add_cat(2, 26, "Male", "Brilliant", "Moonlight", 2008, "G4F001", "black", "A", 
                      dam_id=21, sire_id=22, breed_id=1)
        await add_cat(3, 27, "Female", "Luminous", "Starlight", 2008, "G4M002", "orange", "B", 
                      dam_id=23, sire_id=24, breed_id=2)
        await add_cat(4, 28, "Male", "Shining", "Starlight", 2008, "G4F002", "gray", "B", 
                      dam_id=23, sire_id=24, breed_id=2)
        
        # Generation 8: Glimmer ancestors (2011) - 32 cats (16 pairs of siblings)
        await add_cat(1, 29, "Female", "Glimmer", "Moonlight", 2011, "G3M001", "white", "A", 
                      dam_id=25, sire_id=26, breed_id=1)
        await add_cat(2, 30, "Male", "Sparkle", "Moonlight", 2011, "G3F001", "black", "A", 
                      dam_id=25, sire_id=26, breed_id=1)
        await add_cat(3, 31, "Female", "Twinkle", "Starlight", 2011, "G3M002", "orange", "B", 
                      dam_id=27, sire_id=28, breed_id=2)
        await add_cat(4, 32, "Male", "Glitter", "Starlight", 2011, "G3F002", "gray", "B", 
                      dam_id=27, sire_id=28, breed_id=2)
        
        # Generation 9: Luna ancestors (2014) - 36 cats (18 pairs of siblings)
        await add_cat(1, 33, "Female", "Luna", "Moonlight", 2014, "G2M001", "white", "A", 
                      dam_id=29, sire_id=30, breed_id=1)
        await add_cat(2, 34, "Male", "Shadow", "Moonlight", 2014, "G2F001", "black", "A", 
                      dam_id=29, sire_id=30, breed_id=1)
        await add_cat(3, 35, "Female", "Stella", "Starlight", 2014, "G2M002", "orange", "B", 
                      dam_id=31, sire_id=32, breed_id=2)
        await add_cat(4, 36, "Male", "Thunder", "Starlight", 2014, "G2F002", "gray", "B", 
                      dam_id=31, sire_id=32, breed_id=2)
        
        # Generation 10: Whisper ancestors (2017) - 40 cats (20 pairs of siblings)
        await add_cat(1, 37, "Female", "Whisper", "Moonlight", 2017, "G1M001", "white", "A", 
                      dam_id=33, sire_id=34, breed_id=1)
        await add_cat(2, 38, "Male", "Echo", "Moonlight", 2017, "G1F001", "black", "A", 
                      dam_id=33, sire_id=34, breed_id=1)
        await add_cat(3, 39, "Female", "Sparkle", "Starlight", 2017, "G1M002", "orange", "B", 
                      dam_id=35, sire_id=36, breed_id=2)
        await add_cat(4, 40, "Male", "Flash", "Starlight", 2017, "G1F002", "gray", "B", 
                      dam_id=35, sire_id=36, breed_id=2)
        
        # Generation 11: Parents (2020) - 44 cats (22 pairs of siblings)
        await add_cat(1, 41, "Female", "Misty", "Moonlight", 2020, "M001", "white", "A", 
                      dam_id=37, sire_id=38, breed_id=1)
        await add_cat(2, 42, "Male", "Storm", "Starlight", 2020, "F001", "orange", "B", 
                      dam_id=39, sire_id=40, breed_id=2)
        
        # Generation 12: Current generation (2023) - 200 cats total
        # Main family with 156 cats (78 pairs of siblings)
        for i in range(78):
            cat_id = 43 + i * 2
            sibling_id = cat_id + 1
            
            # Female cat
            await add_cat(1, cat_id, "Female", f"Luna{i+1}", "Moonlight", 2023, f"F{i+1:03d}", "white", "A", 
                          dam_id=41, sire_id=42, breed_id=1)
            
            # Male sibling
            await add_cat(2, sibling_id, "Male", f"Shadow{i+1}", "Moonlight", 2023, f"M{i+1:03d}", "black", "A", 
                          dam_id=41, sire_id=42, breed_id=1)
        
        print("✅ Extended family tree test data added successfully!")
        print("Family structure with 200 cats:")
        print("  Generation 1 (1990): 4 Ancient ancestors")
        print("  Generation 2 (1993): 8 cats (4 pairs of siblings)")
        print("  Generation 3 (1996): 12 cats (6 pairs of siblings)")
        print("  Generation 4 (1999): 16 cats (8 pairs of siblings)")
        print("  Generation 5 (2002): 20 cats (10 pairs of siblings)")
        print("  Generation 6 (2005): 24 cats (12 pairs of siblings)")
        print("  Generation 7 (2008): 28 cats (14 pairs of siblings)")
        print("  Generation 8 (2011): 32 cats (16 pairs of siblings)")
        print("  Generation 9 (2014): 36 cats (18 pairs of siblings)")
        print("  Generation 10 (2017): 40 cats (20 pairs of siblings)")
        print("  Generation 11 (2020): 44 cats (22 pairs of siblings)")
        print("  Generation 12 (2023): 200 cats total (156 siblings from main parents)")
        print("  Total: 200 cats with extensive sibling relationships!")
        print("Main cat ID: 43 (Lightning Thunder)")
        
    except Exception as e:
        print(f"❌ Error adding family tree test data: {e}")
        raise


async def add_test_owners():
    """Add test owners with different permissions"""
    # Admin user
    await add_owner()
    
    # Owner user (permission 2)
    await AsyncOrm.add_owner(
        owner_firstname="John",
        owner_surname="Doe",
        owner_email="john@example.com",
        owner_hashed_password=hash_password("password"),
        owner_permission=2
    )
    
    # Another owner user
    await AsyncOrm.add_owner(
        owner_firstname="Jane",
        owner_surname="Smith",
        owner_email="jane@example.com",
        owner_hashed_password=hash_password("password"),
        owner_permission=2
    )

async def main_add_workflow():
    try:
        await add_permissions()
        await add_test_owners()
        await add_breeds()  # Add breeders
        await add_family_tree_test_data()
        print("✅ Database initialization completed successfully!")
    except Exception as e:
        print(f"❌ Error during database initialization: {e}")
        raise


def start_add_workflow():
    asyncio.run(main_add_workflow())
