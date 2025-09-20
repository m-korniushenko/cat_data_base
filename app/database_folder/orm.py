from datetime import datetime, timedelta, date

import pandas as pd
from app.database_folder.model import (Cat, Owner, History, OwnerPermission, Breed)
from app.database_folder.postgres import async_engine, async_session
from dateutil.relativedelta import relativedelta
from sqlalchemy import (BigInteger, MetaData, Table, and_, asc, cast, delete,
                        desc, text, update, func, or_)
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.future import select
from sqlalchemy.orm import aliased
from logger import log_function_call
from app.niceGUI_folder.pydentic_models import CatCreate, CatUpdate, OwnerCreate, OwnerUpdate


class AsyncOrm:
    @log_function_call
    @staticmethod
    async def get_cat(cat_id: int = None,
                      owner_id: int = None,
                      cat_firstname: str = None,
                      cat_surname: str = None,
                      cat_birthday: datetime = None,
                      cat_microchip_number: str = None,
                      cat_breed_id: str = None,
                      cat_EMS_colour: str = None,
                      cat_gender: str = None,
                      cat_litter: str = None,
                      cat_connection=None,
                      country_city=None):
        query = select(Cat)
        if cat_id:
            query = query.filter_by(cat_id=cat_id)
        if owner_id:
            query = query.filter_by(owner_id=owner_id)
        if cat_firstname:
            query = query.filter_by(cat_firstname=cat_firstname)
        if cat_surname:
            query = query.filter_by(cat_surname=cat_surname)
        if cat_birthday:
            query = query.filter_by(cat_birthday=cat_birthday)
        if cat_microchip_number:
            query = query.filter_by(cat_microchip_number=cat_microchip_number)
        if cat_breed_id:
            query = query.filter_by(cat_breed_id=cat_breed_id)
        if cat_EMS_colour:
            query = query.filter_by(cat_EMS_colour=cat_EMS_colour)
        if cat_gender:
            query = query.filter_by(cat_gender=cat_gender)
        if cat_litter:
            query = query.filter_by(cat_litter=cat_litter)
        if cat_connection:
            query = query.filter_by(cat_connection=cat_connection)
        if country_city:
            query = query.filter_by(country_city=country_city)
        async with async_session() as session:
            result = await session.execute(query)
            rows = []
            for row in result.scalars().all():
                rows.append({"cat_id": row.cat_id,
                             "cat_firstname": row.cat_firstname,
                             "cat_surname": row.cat_surname,
                             "cat_gender": row.cat_gender,
                             "cat_microchip_number": row.cat_microchip_number})
            if cat_id:
                return (len(rows), rows[0] if rows else None)
            return len(rows), rows

    @log_function_call

    # @log_function_call
    @staticmethod
    async def add_cat(owner_id: int, cat_firstname: str, cat_surname: str, cat_gender: str,
                      cat_birthday: datetime, cat_microchip_number: str = None,
                      cat_EMS_colour: str = None, cat_litter: str = None, cat_breed_id: int = None,
                      cat_haritage_number: str = None, cat_dam_id: int = None, cat_sire_id: int = None,
                      cat_photos: list = None, cat_files: list = None,
                      cat_callname: str = None, cat_haritage_number_2: str = None,
                      cat_eye_colour: str = None, cat_hair_type: str = None,
                      cat_tests: str = None, cat_litter_size_male: int = None,
                      cat_litter_size_female: int = None, cat_blood_group: str = None,
                      cat_gencode: str = None, cat_features: str = None,
                      cat_notes: str = None, cat_show_results: str = None,
                      cat_breeding_lock: bool = False, cat_breeding_lock_date: date = None,
                      cat_breeding_animal: bool = False, cat_birth_country: str = None,
                      cat_location: str = None, cat_weight: float = None,
                      cat_birth_weight: float = None, cat_transfer_weight: float = None,
                      cat_faults_deviations: str = None, cat_association: str = None,
                      cat_jaw_fault: str = None, cat_hernia: str = None,
                      cat_testicles: str = None, cat_death_date: date = None,
                      cat_death_cause: str = None, cat_status: str = None,
                      cat_kitten_transfer: bool = False):
        cat_breed_id = int(cat_breed_id) if cat_breed_id else None
        cat_dam_id = int(cat_dam_id) if cat_dam_id else None
        cat_sire_id = int(cat_sire_id) if cat_sire_id else None
        async with async_session() as session:
            new_cat = Cat(
                owner_id=owner_id,
                cat_firstname=cat_firstname,
                cat_surname=cat_surname,
                cat_callname=cat_callname,
                cat_gender=cat_gender,
                cat_birthday=cat_birthday,
                cat_microchip_number=cat_microchip_number,
                cat_breed_id=cat_breed_id,
                cat_EMS_colour=cat_EMS_colour,
                cat_litter=cat_litter,
                cat_haritage_number=cat_haritage_number,
                cat_haritage_number_2=cat_haritage_number_2,
                cat_eye_colour=cat_eye_colour,
                cat_hair_type=cat_hair_type,
                cat_tests=cat_tests,
                cat_litter_size_male=cat_litter_size_male,
                cat_litter_size_female=cat_litter_size_female,
                cat_blood_group=cat_blood_group,
                cat_gencode=cat_gencode,
                cat_features=cat_features,
                cat_notes=cat_notes,
                cat_show_results=cat_show_results,
                cat_breeding_lock=cat_breeding_lock,
                cat_breeding_lock_date=cat_breeding_lock_date,
                cat_breeding_animal=cat_breeding_animal,
                cat_birth_country=cat_birth_country,
                cat_location=cat_location,
                cat_weight=cat_weight,
                cat_birth_weight=cat_birth_weight,
                cat_transfer_weight=cat_transfer_weight,
                cat_faults_deviations=cat_faults_deviations,
                cat_association=cat_association,
                cat_jaw_fault=cat_jaw_fault,
                cat_hernia=cat_hernia,
                cat_testicles=cat_testicles,
                cat_death_date=cat_death_date,
                cat_death_cause=cat_death_cause,
                cat_status=cat_status,
                cat_kitten_transfer=cat_kitten_transfer,
                cat_dam_id=cat_dam_id,
                cat_sire_id=cat_sire_id,
                cat_photos=cat_photos or [],
                cat_files=cat_files or []
            )
            session.add(new_cat)
            await session.commit()
            return new_cat

    @staticmethod
    async def update_cat(cat_id: int, firstname: str, surname: str, gender: str,
                         birthday: datetime, microchip: str = None, colour: str = None,
                         litter: str = None, haritage_number: str = None, owner_id: int = None,
                         breed_id: int = None, dam_id: int = None, sire_id: int = None,
                         cat_photos: list = None, cat_files: list = None,
                         callname: str = None, haritage_number_2: str = None,
                         eye_colour: str = None, hair_type: str = None,
                         tests: str = None, litter_size_male: int = None,
                         litter_size_female: int = None, blood_group: str = None,
                         gencode: str = None, features: str = None,
                         notes: str = None, show_results: str = None,
                         breeding_lock: bool = None, breeding_lock_date: date = None,
                         breeding_animal: bool = None, birth_country: str = None,
                         location: str = None, weight: float = None,
                         birth_weight: float = None, transfer_weight: float = None,
                         faults_deviations: str = None, association: str = None,
                         jaw_fault: str = None, hernia: str = None,
                         testicles: str = None, death_date: date = None,
                         death_cause: str = None, status: str = None,
                         kitten_transfer: bool = None) -> bool:
        """Update cat information"""
        try:
            async with async_session() as session:
                result = await session.execute(select(Cat).filter_by(cat_id=cat_id))
                cat = result.scalar_one_or_none()
                
                if not cat:
                    return False
                
                cat.cat_firstname = firstname
                cat.cat_surname = surname
                cat.cat_callname = callname
                cat.cat_gender = gender
                cat.cat_birthday = birthday
                cat.cat_microchip_number = microchip
                cat.cat_EMS_colour = colour
                cat.cat_litter = litter
                cat.cat_haritage_number = haritage_number
                cat.cat_haritage_number_2 = haritage_number_2
                cat.cat_eye_colour = eye_colour
                cat.cat_hair_type = hair_type
                cat.cat_tests = tests
                cat.cat_litter_size_male = litter_size_male
                cat.cat_litter_size_female = litter_size_female
                cat.cat_blood_group = blood_group
                cat.cat_gencode = gencode
                cat.cat_features = features
                cat.cat_notes = notes
                cat.cat_show_results = show_results
                if breeding_lock is not None:
                    cat.cat_breeding_lock = breeding_lock
                cat.cat_breeding_lock_date = breeding_lock_date
                if breeding_animal is not None:
                    cat.cat_breeding_animal = breeding_animal
                cat.cat_birth_country = birth_country
                cat.cat_location = location
                cat.cat_weight = weight
                cat.cat_birth_weight = birth_weight
                cat.cat_transfer_weight = transfer_weight
                cat.cat_faults_deviations = faults_deviations
                cat.cat_association = association
                cat.cat_jaw_fault = jaw_fault
                cat.cat_hernia = hernia
                cat.cat_testicles = testicles
                cat.cat_death_date = death_date
                cat.cat_death_cause = death_cause
                cat.cat_status = status
                if kitten_transfer is not None:
                    cat.cat_kitten_transfer = kitten_transfer
                cat.owner_id = owner_id
                cat.cat_breed_id = breed_id
                cat.cat_dam_id = dam_id
                cat.cat_sire_id = sire_id
                if cat_photos is not None:
                    cat.cat_photos = cat_photos
                if cat_files is not None:
                    cat.cat_files = cat_files
                
                await session.commit()
                return True
                
        except Exception as e:
            print(f"Error updating cat: {e}")
            import traceback
            traceback.print_exc()
            return False

    @staticmethod
    async def delete_cat(cat_id: int) -> bool:
        """Delete cat by ID"""
        try:
            async with async_session() as session:
                result = await session.execute(select(Cat).filter_by(cat_id=cat_id))
                cat = result.scalar_one_or_none()
                
                if not cat:
                    return False
                
                await session.delete(cat)
                await session.commit()
                return True
                
        except Exception as e:
            print(f"Error deleting cat: {e}")
            return False

    # @log_function_call
    @staticmethod
    async def add_owner(owner_firstname: str, owner_surname: str, owner_email: str, owner_hashed_password: str,
                        owner_permission: int, owner_address: str = None, owner_city: str = None, 
                        owner_country: str = None, owner_zip: str = None, owner_birthday: date = None, 
                        owner_phone: str = None):
        async with async_session() as session:
            new_owner = Owner(
                owner_firstname=owner_firstname, 
                owner_surname=owner_surname, 
                owner_email=owner_email,
                owner_address=owner_address,
                owner_city=owner_city,
                owner_country=owner_country,
                owner_zip=owner_zip,
                owner_birthday=owner_birthday,
                owner_phone=owner_phone,
                owner_permission=owner_permission, 
                owner_hashed_password=owner_hashed_password
            )
            session.add(new_owner)
            await session.commit()
            return new_owner

    @log_function_call
    @staticmethod
    async def get_owner(owner_id: int | None = None,
                        owner_firstname: str | None = None,
                        owner_surname: str | None = None,
                        owner_email: str | None = None,
                        owner_permission: str | None = None):
        query = select(Owner)
        if owner_id is not None:
            query = query.filter_by(owner_id=owner_id)
        if owner_firstname is not None:
            query = query.filter_by(owner_firstname=owner_firstname)
        if owner_surname is not None:
            query = query.filter_by(owner_surname=owner_surname)
        if owner_email is not None:
            query = query.filter_by(owner_email=owner_email)
        if owner_permission is not None:
            query = query.filter_by(owner_permission=owner_permission)

        async with async_session() as session:
            result = await session.execute(query)
            rows = []
            for row in result.scalars().all():
                rows.append({"owner_id": row.owner_id,
                             "owner_firstname": row.owner_firstname,
                             "owner_surname": row.owner_surname,
                             "owner_email": row.owner_email,
                             "owner_hashed_password": row.owner_hashed_password,
                             "owner_address": row.owner_address,
                             "owner_city": row.owner_city,
                             "owner_country": row.owner_country,
                             "owner_zip": row.owner_zip,
                             "owner_birthday": row.owner_birthday,
                             "owner_phone": row.owner_phone,
                             "owner_permission": row.owner_permission})
            if owner_id:
                return (len(rows), rows[0] if rows else None)
            return (len(rows), rows)
            

    @log_function_call
    @staticmethod
    async def update_owner(owner_id: int = None,
                           owner_firstname: str = None,
                           owner_surname: str = None,
                           owner_email: str = None,
                           owner_address: str = None,
                           owner_city: str = None,
                           owner_country: str = None,
                           owner_zip: str = None,
                           owner_birthday: date = None,
                           owner_phone: str = None,
                           owner_permission: int = None):
        async with async_session() as session:
            query = select(Owner).filter_by(owner_id=owner_id)
            result = await session.execute(query)
            owner = result.scalars().first()
            if owner_firstname:
                owner.owner_firstname = owner_firstname
            if owner_surname:
                owner.owner_surname = owner_surname
            if owner_email:
                owner.owner_email = owner_email
            if owner_address:
                owner.owner_address = owner_address
            if owner_city:
                owner.owner_city = owner_city
            if owner_country:
                owner.owner_country = owner_country
            if owner_zip:
                owner.owner_zip = owner_zip
            if owner_birthday:
                owner.owner_birthday = owner_birthday
            if owner_phone:
                owner.owner_phone = owner_phone
            if owner_permission:
                owner.owner_permission = owner_permission
            await session.commit()
            return owner

    @staticmethod
    async def update_owner_dict(owner_id: int, owner_data: dict) -> bool:
        """Update owner information using dictionary"""
        try:
            async with async_session() as session:
                # Get the owner to update
                result = await session.execute(select(Owner).filter_by(owner_id=owner_id))
                owner = result.scalar_one_or_none()
                
                if not owner:
                    return False
                
                # Update fields
                if 'owner_firstname' in owner_data:
                    owner.owner_firstname = owner_data['owner_firstname']
                if 'owner_lastname' in owner_data:
                    owner.owner_surname = owner_data['owner_lastname']
                if 'owner_email' in owner_data:
                    owner.owner_email = owner_data['owner_email']
                if 'owner_phone' in owner_data:
                    owner.owner_phone = owner_data['owner_phone']
                if 'owner_address' in owner_data:
                    owner.owner_address = owner_data['owner_address']
                if 'owner_city' in owner_data:
                    owner.owner_city = owner_data['owner_city']
                if 'owner_country' in owner_data:
                    owner.owner_country = owner_data['owner_country']
                if 'owner_zip' in owner_data:
                    owner.owner_zip = owner_data['owner_zip']
                if 'owner_birthday' in owner_data:
                    owner.owner_birthday = owner_data['owner_birthday']
                if 'owner_permission' in owner_data:
                    owner.owner_permission = owner_data['owner_permission']
                
                await session.commit()
                return True
                
        except Exception as e:
            print(f"Error updating owner: {e}")
            import traceback
            traceback.print_exc()
            return False

    @log_function_call
    @staticmethod
    async def delete_owner(owner_id: int):
        async with async_session() as session:
            query = select(Owner).filter_by(owner_id=owner_id)
            result = await session.execute(query)
            owner = result.scalars().first()
            if owner:
                await session.delete(owner)
                await session.commit()
                return True
            return False

    @log_function_call
    @staticmethod
    async def get_history(history_id: int = None,
                          history_time: datetime = None,
                          cat_id: int = None,
                          user_id: int = None,
                          history_action: str = None):
        query = select(History)
        if history_id:
            query = query.filter_by(history_id=history_id)
        if history_time:
            query = query.filter_by(history_time=history_time)
        if cat_id:
            query = query.filter_by(cat_id=cat_id)
        if user_id:
            query = query.filter_by(user_id=user_id)
        if history_action:
            query = query.filter_by(history_action=history_action)
        async with async_session() as session:
            result = await session.execute(query)
            if len(result.scalars().all()) == 1:
                return result.scalars().first()
            return result.scalars().all()
        
        @log_function_call
        @staticmethod
        async def add_history(history_time: datetime,
                              cat_id: int,
                              user_id: int,
                              history_action: str):
            async with async_session() as session:
                new_history = History(history_time=history_time,
                                      cat_id=cat_id,
                                      user_id=user_id,
                                      history_action=history_action)
                session.add(new_history)
                await session.commit()
                return new_history

    @log_function_call
    @staticmethod
    async def get_cat_connection(cat_id: int):
        async with async_session() as session:
            query = select(CatConnection).filter_by(cat_id=cat_id)
            result = await session.execute(query)
            return result.scalars().all()
        
    @log_function_call
    @staticmethod
    async def add_cat_connection(cat_father_id: int,
                                 cat_mother_id: int):
        async with async_session() as session:
            new_cat_connection = CatConnection(cat_father_id=cat_father_id,
                                               cat_mother_id=cat_mother_id)
            session.add(new_cat_connection)
            await session.commit()
            return new_cat_connection
        
    @log_function_call
    @staticmethod
    async def delete_cat_connection(cat_id: int):
        async with async_session() as session:
            query = select(CatConnection).filter_by(cat_id=cat_id)
            result = await session.execute(query)
            cat_connection = result.scalars().first()
            if cat_connection:
                await session.delete(cat_connection)
                await session.commit()
                return True
            return False
        
    @log_function_call
    @staticmethod
    async def get_cat_type(cat_type_id: int = None,
                           cat_type_name: str = None,
                           cat_type_description: str = None):
        query = select(CatType)
        if cat_type_id:
            query = query.filter_by(cat_type_id=cat_type_id)
        if cat_type_name:
            query = query.filter_by(cat_type_name=cat_type_name)
        if cat_type_description:
            query = query.filter_by(cat_type_description=cat_type_description)
        async with async_session() as session:
            result = await session.execute(query)
            if len(result.scalars().all()) == 1:
                return result.scalars().first()
            return result.scalars().all()
        
    @log_function_call
    @staticmethod
    async def add_cat_type(cat_type_name: str,
                           cat_type_description: str):
        async with async_session() as session: 
            new_cat_type = CatType(cat_type_name=cat_type_name,
                                   cat_type_description=cat_type_description)
            session.add(new_cat_type)
            await session.commit()
            return new_cat_type
        
    @log_function_call
    @staticmethod
    async def delete_cat_type(cat_type_id: int):
        async with async_session() as session:
            query = select(CatType).filter_by(cat_type_id=cat_type_id)
            result = await session.execute(query)
            cat_type = result.scalars().first()
            if cat_type:
                await session.delete(cat_type)
                await session.commit()
                return True
            return False

        
    # @log_function_call
    @staticmethod
    async def add_owner_permission(owner_permission_name: str,
                                   owner_permission_description: str):
        async with async_session() as session:
            new_owner_permission = OwnerPermission(
                owner_permission_name=owner_permission_name, owner_permission_description=owner_permission_description)
            session.add(new_owner_permission)
            await session.commit()
            return new_owner_permission

    @log_function_call
    @staticmethod
    async def get_owner_permission(owner_permission_id: int = None,
                                   owner_permission_name: str = None,
                                   owner_permission_description: str = None):
        query = select(OwnerPermission)
        if owner_permission_id is not None:
            query = query.filter_by(owner_permission_id=owner_permission_id)
        if owner_permission_name is not None:
            query = query.filter_by(owner_permission_name=owner_permission_name)
        if owner_permission_description is not None:
            query = query.filter_by(owner_permission_description=owner_permission_description)

        async with async_session() as session:
            result = await session.execute(query)
            rows = []
            for row in result.scalars().all():
                rows.append({"owner_permission_id": row.owner_permission_id,
                             "owner_permission_name": row.owner_permission_name,
                             "owner_permission_description": row.owner_permission_description})
            if owner_permission_id:
                return (len(rows), rows[0] if rows else None)
            return (len(rows), rows)
        
    @log_function_call
    @staticmethod
    async def delete_user_permission(user_permission_id: int):
        async with async_session() as session:
            query = select(OwnerPermission).filter_by(
                user_permission_id=user_permission_id)
            result = await session.execute(query)
            user_permission = result.scalars().first()
            if user_permission:
                await session.delete(user_permission)
                await session.commit()
                return True
            return False

    @log_function_call
    @staticmethod
    async def get_user(user_id: int = None,
                       user_firstname: str = None,
                       user_surname: str = None,
                       user_mail: str = None,
                       user_permission: str = None):
        query = select(Owner)
        if user_id:
            query = query.filter_by(user_id=user_id)
        if user_firstname:
            query = query.filter_by(user_firstname=user_firstname)
        if user_surname:
            query = query.filter_by(user_surname=user_surname)
        if user_mail:
            query = query.filter_by(user_mail=user_mail)
        if user_permission:
            query = query.filter_by(user_permission=user_permission)
        async with async_session() as session:
            result = await session.execute(query)
            if len(result.scalars().all()) == 1:
                return result.scalars().first()
            return result.scalars().all()

    @log_function_call
    @staticmethod
    async def update_user(user_id: int = None,
                          user_firstname: str = None,
                          user_surname: str = None,
                          user_mail: str = None,
                          user_permission: str = None):
        async with async_session() as session:
            query = select(Owner).filter_by(user_id=user_id)
            result = await session.execute(query)
            user = result.scalars().first()
            if user:
                await session.delete(user)
                await session.commit()
                return True
            return False

    @log_function_call
    @staticmethod
    async def delete_user(user_id: int):
        async with async_session() as session:
            query = select(Owner).filter_by(user_id=user_id)
            result = await session.execute(query)
            user = result.scalars().first()
            if user:
                await session.delete(user)
                await session.commit()
                return True
            return False

    @log_function_call
    @staticmethod
    async def get_cat_info(
        cat_id: int | None = None,
        cat_firstname: str | None = None,
        cat_surname: str | None = None,
        cat_birthday: datetime | None = None,
        cat_microchip_number: str | None = None,
        cat_breed_id: str | None = None,
        cat_EMS_colour: str | None = None,
        cat_gender: str | None = None,
        cat_litter: str | None = None,
        owner_id: int | None = None,
        owner_firstname: str | None = None,
        owner_surname: str | None = None,
        owner_email: str | None = None,
    ):
        # Create aliases for parent cats
        Dam = aliased(Cat)
        Sire = aliased(Cat)
        BreedAlias = aliased(Breed)
        
        query = (
            select(Cat, Owner, Dam, Sire, BreedAlias)
            .join(Owner, Cat.owner_id == Owner.owner_id)
            .outerjoin(Dam, Cat.cat_dam_id == Dam.cat_id)
            .outerjoin(Sire, Cat.cat_sire_id == Sire.cat_id)
            .outerjoin(BreedAlias, Cat.cat_breed_id == BreedAlias.breed_id)
        )
        if cat_id is not None:
            query = query.where(Cat.cat_id == cat_id)
        if cat_firstname:
            query = query.where(Cat.cat_firstname == cat_firstname)
        if cat_surname:
            query = query.where(Cat.cat_surname == cat_surname)
        if cat_birthday:
            query = query.where(Cat.cat_birthday == cat_birthday)
        if cat_microchip_number:
            query = query.where(Cat.cat_microchip_number == cat_microchip_number)
        if cat_breed_id:
            query = query.where(Cat.cat_breed_id == cat_breed_id)
        if cat_EMS_colour:
            query = query.where(Cat.cat_EMS_colour == cat_EMS_colour)
        if cat_gender:
            query = query.where(Cat.cat_gender == cat_gender)
        if cat_litter:
            query = query.where(Cat.cat_litter == cat_litter)
        if owner_id is not None:
            query = query.where(Owner.owner_id == owner_id)
        if owner_firstname:
            query = query.where(Owner.owner_firstname == owner_firstname)
        if owner_surname:
            query = query.where(Owner.owner_surname == owner_surname)
        if owner_email:
            query = query.where(Owner.owner_email == owner_email)

        async with async_session() as session:
            result = await session.execute(query)
            rows = []
            for c, o, d, s, b in result.all():
                rows.append({
                    'id': c.cat_id,
                    'firstname': c.cat_firstname,
                    'surname': c.cat_surname,
                    'gender': c.cat_gender,
                    'birthday': c.cat_birthday,
                    'microchip': c.cat_microchip_number,
                    'breed': c.cat_breed_id,
                    'colour': c.cat_EMS_colour,
                    'litter': c.cat_litter,
                    'haritage_number': c.cat_haritage_number,
                    'owner_id': c.owner_id,
                    'owner_firstname': o.owner_firstname,
                    'owner_surname': o.owner_surname,
                    'owner_email': o.owner_email,
                    'breed_firstname': b.breed_firstname if b else None,
                    'breed_surname': b.breed_surname if b else None,
                    'breed_email': b.breed_email if b else None,
                    'dam': f'{d.cat_firstname} {d.cat_surname}' if d else None,
                    'sire': f'{s.cat_firstname} {s.cat_surname}' if s else None,
                })

        if cat_id is not None:
            return (len(rows), rows[0] if rows else None)
        return (len(rows), rows)

    @log_function_call
    @staticmethod
    async def get_cat_info_like(search: str | None = None):
        # Create aliases for parent cats
        Dam = aliased(Cat)
        Sire = aliased(Cat)
        BreedAlias = aliased(Breed)
        
        query = (
            select(Cat, Owner, Dam, Sire, BreedAlias)
            .join(Owner, Cat.owner_id == Owner.owner_id)
            .outerjoin(Dam, Cat.cat_dam_id == Dam.cat_id)
            .outerjoin(Sire, Cat.cat_sire_id == Sire.cat_id)
            .outerjoin(BreedAlias, Cat.cat_breed_id == BreedAlias.breed_id)
        )

        if search:
            pattern = f"%{search}%"
            query = query.where(
                or_(
                    Cat.cat_firstname.ilike(pattern),
                    Cat.cat_surname.ilike(pattern),
                    Cat.cat_gender.ilike(pattern),
                    Cat.cat_microchip_number.ilike(pattern),
                    Cat.cat_EMS_colour.ilike(pattern),
                    Cat.cat_litter.ilike(pattern),
                    Cat.cat_haritage_number.ilike(pattern),
                    Owner.owner_firstname.ilike(pattern),
                    Owner.owner_surname.ilike(pattern),
                    Owner.owner_email.ilike(pattern),
                    BreedAlias.breed_firstname.ilike(pattern),
                    BreedAlias.breed_surname.ilike(pattern),
                    BreedAlias.breed_email.ilike(pattern),
                )
            )

        async with async_session() as session:
            result = await session.execute(query)
            rows = []
            for c, o, d, s, b in result.all():
                rows.append({
                    'id': c.cat_id,
                    'firstname': c.cat_firstname,
                    'surname': c.cat_surname,
                    'gender': c.cat_gender,
                    'birthday': c.cat_birthday,
                    'microchip': c.cat_microchip_number,
                    'breed': c.cat_breed_id,
                    'colour': c.cat_EMS_colour,
                    'litter': c.cat_litter,
                    'haritage_number': c.cat_haritage_number,
                    'owner_id': c.owner_id,
                    'owner_firstname': o.owner_firstname,
                    'owner_surname': o.owner_surname,
                    'owner_email': o.owner_email,
                    'breed_firstname': b.breed_firstname if b else None,
                    'breed_surname': b.breed_surname if b else None,
                    'breed_email': b.breed_email if b else None,
                    'dam': f'{d.cat_firstname} {d.cat_surname}' if d else None,
                    'sire': f'{s.cat_firstname} {s.cat_surname}' if s else None,
                })

        print(f"get_cat_info_like returned {len(rows)} rows")
        return (len(rows), rows)

    @log_function_call
    @staticmethod
    async def get_breed_count():
        """Get total count of breeds"""
        async with async_session() as session:
            result = await session.execute(select(func.count(Breed.breed_id)))
            return result.scalar()

    @log_function_call
    @staticmethod
    async def add_breed(breed_firstname: str, breed_surname: str, breed_email: str,
                        breed_gender: str = None, breed_birthday: date = None, breed_address: str = None,
                        breed_city: str = None, breed_country: str = None, breed_zip: str = None,
                        breed_phone: str = None, breed_description: str = None):
        async with async_session() as session:
            new_breed = Breed(
                breed_firstname=breed_firstname,
                breed_surname=breed_surname,
                breed_gender=breed_gender,
                breed_birthday=breed_birthday,
                breed_address=breed_address,
                breed_city=breed_city,
                breed_country=breed_country,
                breed_zip=breed_zip,
                breed_phone=breed_phone,
                breed_email=breed_email,
                breed_description=breed_description
            )
            session.add(new_breed)
            await session.commit()
            return new_breed

    @log_function_call
    @staticmethod
    async def get_breed(breed_id: int = None,
                        breed_firstname: str = None,
                        breed_surname: str = None,
                        breed_email: str = None):
        query = select(Breed)
        if breed_id is not None:
            query = query.filter_by(breed_id=breed_id)
        if breed_firstname is not None:
            query = query.filter_by(breed_firstname=breed_firstname)
        if breed_surname is not None:
            query = query.filter_by(breed_surname=breed_surname)
        if breed_email is not None:
            query = query.filter_by(breed_email=breed_email)

        async with async_session() as session:
            result = await session.execute(query)
            rows = []
            for row in result.scalars().all():
                rows.append({"breed_id": row.breed_id,
                             "breed_firstname": row.breed_firstname,
                             "breed_surname": row.breed_surname,
                             "breed_gender": row.breed_gender,
                             "breed_birthday": row.breed_birthday,
                             "breed_address": row.breed_address,
                             "breed_city": row.breed_city,
                             "breed_country": row.breed_country,
                             "breed_zip": row.breed_zip,
                             "breed_phone": row.breed_phone,
                             "breed_email": row.breed_email,
                             "breed_description": row.breed_description})
            if breed_id:
                return (len(rows), rows[0] if rows else None)
            return (len(rows), rows)

    @staticmethod
    async def get_owner_by_id(owner_id: int):
        """Get owner by ID"""
        try:
            async with async_session() as session:
                result = await session.execute(select(Owner).filter_by(owner_id=owner_id))
                return result.scalar_one_or_none()
        except Exception as e:
            print(f"Error getting owner by ID: {e}")
            return None

    @staticmethod
    async def get_breed_by_id(breed_id: int):
        """Get breed by ID"""
        try:
            async with async_session() as session:
                result = await session.execute(select(Breed).filter_by(breed_id=breed_id))
                return result.scalar_one_or_none()
        except Exception as e:
            print(f"Error getting breed by ID: {e}")
            return None

    @staticmethod
    async def update_breed(breed_id: int, breed_data: dict) -> bool:
        """Update breed information"""
        try:
            async with async_session() as session:
                # Get the breed to update
                result = await session.execute(select(Breed).filter_by(breed_id=breed_id))
                breed = result.scalar_one_or_none()
                
                if not breed:
                    return False
                
                # Update fields
                if 'breed_firstname' in breed_data:
                    breed.breed_firstname = breed_data['breed_firstname']
                if 'breed_lastname' in breed_data:
                    breed.breed_surname = breed_data['breed_lastname']
                if 'breed_email' in breed_data:
                    breed.breed_email = breed_data['breed_email']
                if 'breed_phone' in breed_data:
                    breed.breed_phone = breed_data['breed_phone']
                if 'breed_address' in breed_data:
                    breed.breed_address = breed_data['breed_address']
                if 'breed_city' in breed_data:
                    breed.breed_city = breed_data['breed_city']
                if 'breed_country' in breed_data:
                    breed.breed_country = breed_data['breed_country']
                if 'breed_zip' in breed_data:
                    breed.breed_zip = breed_data['breed_zip']
                if 'breed_birthday' in breed_data:
                    breed.breed_birthday = breed_data['breed_birthday']
                if 'breed_gender' in breed_data:
                    breed.breed_gender = breed_data['breed_gender']
                if 'breed_description' in breed_data:
                    breed.breed_description = breed_data['breed_description']
                
                await session.commit()
                return True
                
        except Exception as e:
            print(f"Error updating breed: {e}")
            import traceback
            traceback.print_exc()
            return False

    @staticmethod
    async def delete_breed(breed_id: int) -> bool:
        """Delete breed by ID"""
        try:
            async with async_session() as session:
                result = await session.execute(select(Breed).filter_by(breed_id=breed_id))
                breed = result.scalar_one_or_none()
                
                if not breed:
                    return False
                
                await session.delete(breed)
                await session.commit()
                return True
                
        except Exception as e:
            print(f"Error deleting breed: {e}")
            return False

    @log_function_call
    @staticmethod
    async def get_cat_with_parents(cat_id: int):
        """Get cat information with parent details"""
        async with async_session() as session:
            # Get the main cat
            cat_query = select(Cat).where(Cat.cat_id == cat_id)
            cat_result = await session.execute(cat_query)
            cat = cat_result.scalars().first()
            
            if not cat:
                return None
                
            # Get owner information
            owner_query = select(Owner).where(Owner.owner_id == cat.owner_id)
            owner_result = await session.execute(owner_query)
            owner = owner_result.scalars().first()
            
            # Get breed information
            breed_query = select(Breed).where(Breed.breed_id == cat.cat_breed_id)
            breed_result = await session.execute(breed_query)
            breed = breed_result.scalars().first()
            
            # Get dam (mother) information
            dam = None
            if cat.cat_dam_id:
                dam_query = select(Cat).where(Cat.cat_id == cat.cat_dam_id)
                dam_result = await session.execute(dam_query)
                dam = dam_result.scalars().first()
            
            # Get sire (father) information
            sire = None
            if cat.cat_sire_id:
                sire_query = select(Cat).where(Cat.cat_id == cat.cat_sire_id)
                sire_result = await session.execute(sire_query)
                sire = sire_result.scalars().first()
            
            return {
                'cat': cat,
                'owner': owner,
                'breed': breed,
                'dam': dam,
                'sire': sire
            }

    @log_function_call
    @staticmethod
    async def get_cat_family_tree(cat_id: int, max_depth: int = 3):
        """Get family tree for a cat up to specified depth"""
        async with async_session() as session:
            def get_cat_info(cat):
                if not cat:
                    return None
                return {
                    'id': cat.cat_id,
                    'firstname': cat.cat_firstname,
                    'surname': cat.cat_surname,
                    'gender': cat.cat_gender,
                    'birthday': cat.cat_birthday,
                    'microchip': cat.cat_microchip_number
                }
            
            async def build_tree(current_cat_id, depth):
                if depth > max_depth or not current_cat_id:
                    return None
                    
                cat_query = select(Cat).where(Cat.cat_id == current_cat_id)
                cat_result = await session.execute(cat_query)
                cat = cat_result.scalars().first()
                
                if not cat:
                    return None
                
                tree_node = get_cat_info(cat)
                tree_node['dam'] = await build_tree(cat.cat_dam_id, depth + 1)
                tree_node['sire'] = await build_tree(cat.cat_sire_id, depth + 1)
                
                return tree_node
            
            return await build_tree(cat_id, 0)