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
                  colour="black", litter="A", dam_id=None, sire_id=None, breed_id=1,
                  callname=None, title=None, eye_colour=None, hair_type=None,
                  tests=None, litter_size_male=None, litter_size_female=None,
                  blood_group=None, gencode=None, features=None, notes=None,
                  show_results=None, breeding_lock=False, breeding_lock_date=None,
                  breeding_animal=False, birth_country=None, location=None,
                  weight=None, birth_weight=None, transfer_weight=None,
                  faults_deviations=None, association=None, jaw_fault=None,
                  hernia=None, testicles=None, death_date=None, death_cause=None,
                  status=None, kitten_transfer=False):
    return await AsyncOrm.add_cat(
        owner_id=owner_id, 
        cat_firstname=firstname, 
        cat_surname=surname,
        cat_callname=callname,
        cat_gender=gender,
        cat_birthday=date(birthday_year, 5, 17), 
        cat_microchip_number=microchip,
        cat_title=[title] if title else None,
        cat_EMS_colour=colour,
        cat_litter=litter,
        cat_haritage_number=f"SB{idx:04d}",
        cat_haritage_number_2=f"SB2{idx:04d}" if idx % 2 == 0 else None,
        cat_eye_colour=eye_colour,
        cat_hair_type=hair_type,
        cat_tests=tests,
        cat_litter_size_male=litter_size_male,
        cat_litter_size_female=litter_size_female,
        cat_blood_group=blood_group,
        cat_gencode=gencode,
        cat_features=features,
        cat_notes=notes,
        cat_show_results=show_results,
        cat_breeding_lock=breeding_lock,
        cat_breeding_lock_date=breeding_lock_date,
        cat_breeding_animal=breeding_animal,
        cat_birth_country=birth_country,
        cat_location=location,
        cat_weight=weight,
        cat_birth_weight=birth_weight,
        cat_transfer_weight=transfer_weight,
        cat_faults_deviations=faults_deviations,
        cat_association=association,
        cat_jaw_fault=jaw_fault,
        cat_hernia=hernia,
        cat_testicles=testicles,
        cat_death_date=death_date,
        cat_death_cause=death_cause,
        cat_status=status,
        cat_kitten_transfer=kitten_transfer,
        cat_dam_id=dam_id,
        cat_sire_id=sire_id,
        cat_breed_id=breed_id
    )


async def add_breeds():
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
        await AsyncOrm.add_breed(
            breed_firstname="Golden",
            breed_surname="Paws",
            breed_email="golden@paws.com", 
            breed_phone="+1122334455",
            breed_description="Golden standard breeding"
        )
        await AsyncOrm.add_breed(
            breed_firstname="Silver",
            breed_surname="Whiskers",
            breed_email="silver@whiskers.com", 
            breed_phone="+5566778899",
            breed_description="Silver premium breeding"
        )
        await AsyncOrm.add_breed(
            breed_firstname="Diamond",
            breed_surname="Cats",
            breed_email="diamond@cats.com", 
            breed_phone="+9988776655",
            breed_description="Diamond quality breeding"
        )
        print("✅ Breeders added successfully!")
    except Exception as e:
        print(f"❌ Error adding breeders: {e}")


async def add_cat_with_random_data(owner_id, idx, gender, firstname, surname, birthday_year, microchip, 
                                  colour="black", litter="A", dam_id=None, sire_id=None, breed_id=1):
    """Add cat with random generated data for all fields"""
    data = get_random_cat_data(idx)
    return await add_cat(
        owner_id=owner_id, idx=idx, gender=gender, firstname=firstname, surname=surname,
        birthday_year=birthday_year, microchip=microchip, colour=colour, litter=litter,
        dam_id=dam_id, sire_id=sire_id, breed_id=breed_id, **data
    )


def get_random_cat_data(idx):
    """Generate random cat data for testing filters"""
    import random
    
    # Colors
    colors = ["black", "white", "orange", "gray", "brown", "cream", "silver", "blue", "red", "chocolate"]
    eye_colors = ["Blue", "Green", "Yellow", "Orange", "Heterochromatic"]
    hair_types = ["Short Hair", "Long Hair", "Semi-Long Hair"]
    titles = ["Champion", "Grand Champion", "Supreme Grand Champion"]
    countries = ["Germany", "USA", "UK", "France", "Netherlands", "Poland", "Russia"]
    associations = ["CFA", "TICA", "FIFe", "WCF", "GCCF"]
    statuses = ["Alive", "Deceased", "Missing", "Transferred"]
    jaw_faults = ["None", "Overbite", "Underbite", "Crossbite"]
    hernias = ["None", "Umbilical", "Inguinal", "Diaphragmatic"]
    testicles_status = ["Normal", "Cryptorchid", "Monorchid"]
    
    # Random selections
    eye_color = random.choice(eye_colors)
    hair_type = random.choice(hair_types)
    title = random.choice(titles) if random.random() < 0.3 else None
    country = random.choice(countries)
    association = random.choice(associations)
    status = random.choice(statuses)
    
    # Weights (in kg)
    weight = round(random.uniform(2.5, 8.0), 1) if random.random() < 0.8 else None
    birth_weight = round(random.uniform(80, 120), 1) if random.random() < 0.7 else None
    transfer_weight = round(random.uniform(90, 130), 1) if random.random() < 0.6 else None
    
    # Litter sizes
    litter_male = random.randint(0, 6) if random.random() < 0.5 else None
    litter_female = random.randint(0, 6) if random.random() < 0.5 else None
    
    # Breeding status
    breeding_animal = random.choice([True, False])
    breeding_lock = random.choice([True, False]) if random.random() < 0.2 else False
    kitten_transfer = random.choice([True, False]) if random.random() < 0.1 else False
    
    # Health data
    jaw_fault = random.choice(jaw_faults)
    hernia = random.choice(hernias)
    testicles = random.choice(testicles_status) if random.random() < 0.7 else None
    
    # Death data (10% chance)
    death_date = None
    death_cause = None
    if status == "Deceased" and random.random() < 0.1:
        death_date = date(2023, random.randint(1, 12), random.randint(1, 28))
        death_cause = random.choice(["Old age", "Illness", "Accident", "Unknown"])
    
    return {
        "callname": f"Kitty{idx}" if random.random() < 0.7 else None,
        "title": title,
        "eye_colour": eye_color,
        "hair_type": hair_type,
        "tests": f"DNA{idx:03d}" if random.random() < 0.4 else None,
        "litter_size_male": litter_male,
        "litter_size_female": litter_female,
        "blood_group": f"Type {random.choice(['A', 'B', 'AB'])}" if random.random() < 0.3 else None,
        "gencode": f"GEN{idx:03d}" if random.random() < 0.2 else None,
        "features": f"Special markings on {random.choice(['head', 'tail', 'back'])}" if random.random() < 0.3 else None,
        "notes": f"Friendly and playful cat #{idx}" if random.random() < 0.5 else None,
        "show_results": "Best in Show 2023" if random.random() < 0.1 else None,
        "breeding_lock": breeding_lock,
        "breeding_lock_date": date(2023, 1, 1) if breeding_lock else None,
        "breeding_animal": breeding_animal,
        "birth_country": country,
        "location": f"{country} Cattery" if random.random() < 0.6 else None,
        "weight": weight,
        "birth_weight": birth_weight,
        "transfer_weight": transfer_weight,
        "faults_deviations": f"Minor {random.choice(['ear', 'tail', 'coat'])} issue" if random.random() < 0.2 else None,
        "association": association,
        "jaw_fault": jaw_fault,
        "hernia": hernia,
        "testicles": testicles,
        "death_date": death_date,
        "death_cause": death_cause,
        "status": status,
        "kitten_transfer": kitten_transfer
    }


async def add_family_tree_test_data():
    """Add test data for family tree visualization - 200 cats with siblings"""
    try:
        # Add only 5 owners
        for i in range(5):
            await add_owner()
        
        # Add breeders (moved to main init)
        
        # Generation 1: Ancient ancestors (1990) - 4 cats with diverse data
        await add_cat_with_random_data(1, 1, "Female", "Ancient", "Moonlight", 1990, "G10M001", "white", "A", breed_id=1)
        await add_cat_with_random_data(2, 2, "Male", "Elder", "Moonlight", 1990, "G10F001", "black", "A", breed_id=1)
        await add_cat_with_random_data(3, 3, "Female", "Primordial", "Starlight", 1990, "G10M002", "orange", "B", breed_id=2)
        await add_cat_with_random_data(4, 4, "Male", "Ancestor", "Starlight", 1990, "G10F002", "gray", "B", breed_id=2)
        
        # Generation 2: Venerable ancestors (1993) - 8 cats (4 pairs of siblings)
        await add_cat_with_random_data(1, 5, "Female", "Venerable", "Moonlight", 1993, "G9M001", "white", "A", 
                                      dam_id=1, sire_id=2, breed_id=1)
        await add_cat_with_random_data(2, 6, "Male", "Sage", "Moonlight", 1993, "G9F001", "black", "A", 
                                      dam_id=1, sire_id=2, breed_id=1)
        await add_cat_with_random_data(3, 7, "Female", "Noble", "Starlight", 1993, "G9M002", "orange", "B", 
                                      dam_id=3, sire_id=4, breed_id=2)
        await add_cat_with_random_data(4, 8, "Male", "Royal", "Starlight", 1993, "G9F002", "gray", "B", 
                                      dam_id=3, sire_id=4, breed_id=2)
        
        # Generation 3: Majestic ancestors (1996) - 12 cats (6 pairs of siblings)
        await add_cat_with_random_data(1, 9, "Female", "Majestic", "Moonlight", 1996, "G8M001", "white", "A", 
                                      dam_id=5, sire_id=6, breed_id=1)
        await add_cat_with_random_data(2, 10, "Male", "Imperial", "Moonlight", 1996, "G8F001", "black", "A", 
                                      dam_id=5, sire_id=6, breed_id=1)
        await add_cat_with_random_data(3, 11, "Female", "Regal", "Starlight", 1996, "G8M002", "orange", "B", 
                                      dam_id=7, sire_id=8, breed_id=2)
        await add_cat_with_random_data(4, 12, "Male", "Supreme", "Starlight", 1996, "G8F002", "gray", "B", 
                                      dam_id=7, sire_id=8, breed_id=2)
        
        # Generation 4: Divine ancestors (1999) - 16 cats (8 pairs of siblings)
        await add_cat_with_random_data(1, 13, "Female", "Divine", "Moonlight", 1999, "G7M001", "white", "A", 
                                      dam_id=9, sire_id=10, breed_id=1)
        await add_cat_with_random_data(2, 14, "Male", "Celestial", "Moonlight", 1999, "G7F001", "black", "A", 
                                      dam_id=9, sire_id=10, breed_id=1)
        await add_cat_with_random_data(3, 15, "Female", "Ethereal", "Starlight", 1999, "G7M002", "orange", "B", 
                                      dam_id=11, sire_id=12, breed_id=2)
        await add_cat_with_random_data(4, 16, "Male", "Cosmic", "Starlight", 1999, "G7F002", "gray", "B", 
                                      dam_id=11, sire_id=12, breed_id=2)
        
        # Generation 5: Mystic ancestors (2002) - 20 cats (10 pairs of siblings)
        await add_cat_with_random_data(1, 17, "Female", "Mystic", "Moonlight", 2002, "G6M001", "white", "A", 
                                      dam_id=13, sire_id=14, breed_id=1)
        await add_cat_with_random_data(2, 18, "Male", "Enchanted", "Moonlight", 2002, "G6F001", "black", "A", 
                                      dam_id=13, sire_id=14, breed_id=1)
        await add_cat_with_random_data(3, 19, "Female", "Magical", "Starlight", 2002, "G6M002", "orange", "B", 
                                      dam_id=15, sire_id=16, breed_id=2)
        await add_cat_with_random_data(4, 20, "Male", "Spellbound", "Starlight", 2002, "G6F002", "gray", "B", 
                                      dam_id=15, sire_id=16, breed_id=2)
        
        # Generation 6: Enchanted ancestors (2005) - 24 cats (12 pairs of siblings)
        await add_cat_with_random_data(1, 21, "Female", "Enchanted", "Moonlight", 2005, "G5M001", "white", "A", 
                                      dam_id=17, sire_id=18, breed_id=1)
        await add_cat_with_random_data(2, 22, "Male", "Mystical", "Moonlight", 2005, "G5F001", "black", "A", 
                                      dam_id=17, sire_id=18, breed_id=1)
        await add_cat_with_random_data(3, 23, "Female", "Wondrous", "Starlight", 2005, "G5M002", "orange", "B", 
                                      dam_id=19, sire_id=20, breed_id=2)
        await add_cat_with_random_data(4, 24, "Male", "Marvelous", "Starlight", 2005, "G5F002", "gray", "B", 
                                      dam_id=19, sire_id=20, breed_id=2)
        
        # Generation 7: Radiant ancestors (2008) - 28 cats (14 pairs of siblings)
        await add_cat_with_random_data(1, 25, "Female", "Radiant", "Moonlight", 2008, "G4M001", "white", "A", 
                                      dam_id=21, sire_id=22, breed_id=1)
        await add_cat_with_random_data(2, 26, "Male", "Brilliant", "Moonlight", 2008, "G4F001", "black", "A", 
                                      dam_id=21, sire_id=22, breed_id=1)
        await add_cat_with_random_data(3, 27, "Female", "Luminous", "Starlight", 2008, "G4M002", "orange", "B", 
                                      dam_id=23, sire_id=24, breed_id=2)
        await add_cat_with_random_data(4, 28, "Male", "Shining", "Starlight", 2008, "G4F002", "gray", "B", 
                                      dam_id=23, sire_id=24, breed_id=2)
        
        # Generation 8: Glimmer ancestors (2011) - 32 cats (16 pairs of siblings)
        await add_cat_with_random_data(1, 29, "Female", "Glimmer", "Moonlight", 2011, "G3M001", "white", "A", 
                                      dam_id=25, sire_id=26, breed_id=1)
        await add_cat_with_random_data(2, 30, "Male", "Sparkle", "Moonlight", 2011, "G3F001", "black", "A", 
                                      dam_id=25, sire_id=26, breed_id=1)
        await add_cat_with_random_data(3, 31, "Female", "Twinkle", "Starlight", 2011, "G3M002", "orange", "B", 
                                      dam_id=27, sire_id=28, breed_id=2)
        await add_cat_with_random_data(4, 32, "Male", "Glitter", "Starlight", 2011, "G3F002", "gray", "B", 
                                      dam_id=27, sire_id=28, breed_id=2)
        
        # Generation 9: Luna ancestors (2014) - 36 cats (18 pairs of siblings)
        await add_cat_with_random_data(1, 33, "Female", "Luna", "Moonlight", 2014, "G2M001", "white", "A", 
                                      dam_id=29, sire_id=30, breed_id=1)
        await add_cat_with_random_data(2, 34, "Male", "Shadow", "Moonlight", 2014, "G2F001", "black", "A", 
                                      dam_id=29, sire_id=30, breed_id=1)
        await add_cat_with_random_data(3, 35, "Female", "Stella", "Starlight", 2014, "G2M002", "orange", "B", 
                                      dam_id=31, sire_id=32, breed_id=2)
        await add_cat_with_random_data(4, 36, "Male", "Thunder", "Starlight", 2014, "G2F002", "gray", "B", 
                                      dam_id=31, sire_id=32, breed_id=2)
        
        # Generation 10: Whisper ancestors (2017) - 40 cats (20 pairs of siblings)
        await add_cat_with_random_data(1, 37, "Female", "Whisper", "Moonlight", 2017, "G1M001", "white", "A", 
                                      dam_id=33, sire_id=34, breed_id=1)
        await add_cat_with_random_data(2, 38, "Male", "Echo", "Moonlight", 2017, "G1F001", "black", "A", 
                                      dam_id=33, sire_id=34, breed_id=1)
        await add_cat_with_random_data(3, 39, "Female", "Sparkle", "Starlight", 2017, "G1M002", "orange", "B", 
                                      dam_id=35, sire_id=36, breed_id=2)
        await add_cat_with_random_data(4, 40, "Male", "Flash", "Starlight", 2017, "G1F002", "gray", "B", 
                                      dam_id=35, sire_id=36, breed_id=2)
        
        # Generation 11: Parents (2020) - 44 cats (22 pairs of siblings)
        await add_cat_with_random_data(1, 41, "Female", "Misty", "Moonlight", 2020, "M001", "white", "A", 
                                      dam_id=37, sire_id=38, breed_id=1)
        await add_cat_with_random_data(2, 42, "Male", "Storm", "Starlight", 2020, "F001", "orange", "B", 
                                      dam_id=39, sire_id=40, breed_id=2)
        
        # Generation 12: Current generation (2023) - 200 cats total
        # Main family with 156 cats (78 pairs of siblings)
        for i in range(78):
            cat_id = 43 + i * 2
            sibling_id = cat_id + 1
            
            # Female cat
            await add_cat_with_random_data(1, cat_id, "Female", f"Luna{i+1}", "Moonlight", 2023, f"F{i+1:03d}", 
                                          "white", "A", dam_id=41, sire_id=42, breed_id=1)
            
            # Male sibling
            await add_cat_with_random_data(2, sibling_id, "Male", f"Shadow{i+1}", "Moonlight", 2023, f"M{i+1:03d}", 
                                          "black", "A", dam_id=41, sire_id=42, breed_id=1)
        
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
    
    # Additional owners for testing
    await AsyncOrm.add_owner(
        owner_firstname="Bob",
        owner_surname="Johnson",
        owner_email="bob@example.com",
        owner_hashed_password=hash_password("password"),
        owner_permission=2
    )
    
    await AsyncOrm.add_owner(
        owner_firstname="Alice",
        owner_surname="Wilson",
        owner_email="alice@example.com",
        owner_hashed_password=hash_password("password"),
        owner_permission=2
    )
    
    await AsyncOrm.add_owner(
        owner_firstname="Charlie",
        owner_surname="Brown",
        owner_email="charlie@example.com",
        owner_hashed_password=hash_password("password"),
        owner_permission=2
    )


async def add_diverse_test_cats():
    """Add diverse test cats with different owners for filter testing"""
    try:
        # Add cats with different owners (IDs 2-6) and breeders (IDs 1-5)
        owners = [2, 3, 4, 5, 6]
        breeders = [1, 2, 3, 4, 5]  # Now we have 5 breeders
        
        # Add 50 diverse cats
        for i in range(50):
            owner_id = owners[i % len(owners)]
            breed_id = breeders[i % len(breeders)]  # Use different breeders
            data = get_random_cat_data(300 + i)
            
            # Vary birth years
            birth_year = 2018 + (i % 6)  # 2018-2023
            
            await add_cat(
                owner_id=owner_id,
                idx=300 + i,
                gender="Female" if i % 2 == 0 else "Male",
                firstname=f"TestCat{i+1}",
                surname="TestSurname",
                birthday_year=birth_year,
                microchip=f"TEST{i+1:03d}",
                colour=data.get("colour", "black"),
                litter=f"L{i+1}",
                breed_id=breed_id,
                **data
            )
        
        print("✅ Diverse test cats added successfully!")
        
    except Exception as e:
        print(f"❌ Error adding diverse test cats: {e}")
        raise


async def main_add_workflow():
    try:
        await add_permissions()
        await add_test_owners()
        await add_breeds()  # Add breeders
        await add_family_tree_test_data()
        await add_diverse_test_cats()  # Add diverse cats for filter testing
        print("✅ Database initialization completed successfully!")
        print("📊 Test data summary:")
        print("  - 6 Owners (1 admin, 5 regular users)")
        print("  - 5 Breeders (Elite Cattery, Royal Breeders, Golden Paws, Silver Whiskers, Diamond Cats)")
        print("  - 200 Family tree cats")
        print("  - 50 Diverse test cats")
        print("  - Total: 250 cats with extensive filter data!")
    except Exception as e:
        print(f"❌ Error during database initialization: {e}")
        raise


def start_add_workflow():
    asyncio.run(main_add_workflow())
