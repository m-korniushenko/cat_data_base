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
    @staticmethod
    async def update_cat(cat_id: int = None,
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
        async with async_session() as session:
            query = select(Cat).filter_by(cat_id=cat_id)
            result = await session.execute(query)
            cat = result.scalars().first()
            if cat_firstname:
                cat.cat_firstname = cat_firstname
            if cat_surname:
                cat.cat_surname = cat_surname
            if cat_birthday:
                cat.cat_birthday = cat_birthday
            if cat_microchip_number:
                cat.cat_microchip_number = cat_microchip_number
            if cat_breed_id:
                cat.cat_breed_id = cat_breed_id
            if cat_EMS_colour:
                cat.cat_EMS_colour = cat_EMS_colour
            if cat_gender:
                cat.cat_gender = cat_gender
            if cat_litter:
                cat.cat_litter = cat_litter
            if cat_connection:
                cat.cat_connection = cat_connection
            if country_city:
                cat.country_city = country_city
            await session.commit()
            return cat

    @log_function_call
    @staticmethod
    async def delete_cat(cat_id: int):
        async with async_session() as session:
            query = select(Cat).filter_by(cat_id=cat_id)
            result = await session.execute(query)
            cat = result.scalars().first()
            if cat:
                await session.delete(cat)
                await session.commit()
                return True
            return False

    # @log_function_call
    @staticmethod
    async def add_cat(owner_id: int, cat_firstname: str, cat_surname: str, cat_gender: str,
                      cat_birthday: datetime, cat_microchip_number: str,
                      cat_EMS_colour: str, cat_litter: str, cat_id: int = None, cat_breed_id: int = None):
        cat_breed_id = int(cat_breed_id) if cat_breed_id else None
        async with async_session() as session:
            new_cat = Cat(
                owner_id=owner_id,
                cat_firstname=cat_firstname,
                cat_surname=cat_surname,
                cat_gender=cat_gender,
                cat_birthday=cat_birthday,
                cat_microchip_number=cat_microchip_number,
                cat_breed_id=cat_breed_id,
                cat_EMS_colour=cat_EMS_colour,
                cat_litter=cat_litter
            )
            if cat_id:
                new_cat.cat_id = cat_id
            session.add(new_cat)
            await session.commit()
            return new_cat

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
        query = (
            select(Cat, Owner)
            .join(Owner, Cat.owner_id == Owner.owner_id)
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
            for c, o in result.all():
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
                    'owner_id': c.owner_id,
                    'owner_firstname': o.owner_firstname,
                    'owner_surname': o.owner_surname,
                    'owner_email': o.owner_email,
                })

        if cat_id is not None:
            return (len(rows), rows[0] if rows else None)
        return (len(rows), rows)

    @log_function_call
    @staticmethod
    async def get_cat_info_like(search: str | None = None):
        query = (
            select(Cat, Owner)
            .join(Owner, Cat.owner_id == Owner.owner_id)
        )

        if search:
            pattern = f"%{search}%"
            query = query.where(
                or_(
                    Cat.cat_firstname.ilike(pattern),
                    Cat.cat_surname.ilike(pattern),
                    Cat.cat_gender.ilike(pattern),
                    Cat.cat_microchip_number.ilike(pattern),
                    Cat.cat_breed_id.ilike(pattern),
                    Cat.cat_EMS_colour.ilike(pattern),
                    Cat.cat_litter.ilike(pattern),
                    Owner.owner_firstname.ilike(pattern),
                    Owner.owner_surname.ilike(pattern),
                    Owner.owner_email.ilike(pattern),
                )
            )

        async with async_session() as session:
            result = await session.execute(query)
            rows = []
            for c, o in result.all():
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
                    'owner_id': c.owner_id,
                    'owner_firstname': o.owner_firstname,
                    'owner_surname': o.owner_surname,
                    'owner_email': o.owner_email,
                })

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