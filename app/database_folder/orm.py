from datetime import datetime, timedelta

import pandas as pd
from app.database_folder.model import (Cat, Owner, History, CatConnection,
                                       CatType, UserPermission, CountryCity)
from database_folder.postgres import async_engine, async_session
from dateutil.relativedelta import relativedelta
from sqlalchemy import (BigInteger, MetaData, Table, and_, asc, cast, delete,
                        desc, text, update, func)
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.future import select
from sqlalchemy.orm import aliased
from logger import log_function_call


class AsyncOrm:
    @log_function_call
    @staticmethod
    async def get_cat(cat_id: int = None,
                      owner_id: int = None,
                      cat_firstname: str = None,
                      cat_surname: str = None,
                      cat_birthday: datetime = None,
                      cat_microchip_number: str = None,
                      cat_breed: str = None,
                      cat_colour: str = None,
                      cat_gender: str = None,
                      cat_litter: str = None,
                      cat_ifc: str = None,
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
        if cat_breed:
            query = query.filter_by(cat_breed=cat_breed)
        if cat_colour:
            query = query.filter_by(cat_colour=cat_colour)
        if cat_gender:
            query = query.filter_by(cat_gender=cat_gender)
        if cat_litter:
            query = query.filter_by(cat_litter=cat_litter)
        if cat_ifc:
            query = query.filter_by(cat_ifc=cat_ifc)
        if cat_connection:
            query = query.filter_by(cat_connection=cat_connection)
        if country_city:
            query = query.filter_by(country_city=country_city)
        async with async_session() as session:
            result = await session.execute(query)
            if len(result.scalars().all()) == 1:
                return result.scalars().first()
            return result.scalars().all()

    @log_function_call
    @staticmethod
    async def update_cat(cat_id: int = None,
                         cat_firstname: str = None,
                         cat_surname: str = None,
                         cat_birthday: datetime = None,
                         cat_microchip_number: str = None,
                         cat_breed: str = None,
                         cat_colour: str = None,
                         cat_gender: str = None,
                         cat_litter: str = None,
                         cat_ifc: str = None,
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
            if cat_breed:
                cat.cat_breed = cat_breed
            if cat_colour:
                cat.cat_colour = cat_colour
            if cat_gender:
                cat.cat_gender = cat_gender
            if cat_litter:
                cat.cat_litter = cat_litter
            if cat_ifc:
                cat.cat_ifc = cat_ifc
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

    @log_function_call
    @staticmethod
    async def get_owner(owner_id: int = None,
                        owner_firstname: str = None,
                        owner_surname: str = None,
                        owner_mail: str = None,
                        owner_permission: str = None):
        query = select(Owner)
        if owner_id:
            query = query.filter_by(owner_id=owner_id)
        if owner_firstname:
            query = query.filter_by(owner_firstname=owner_firstname)
        if owner_surname:
            query = query.filter_by(owner_surname=owner_surname)
        if owner_mail:
            query = query.filter_by(owner_mail=owner_mail)
        if owner_permission:
            query = query.filter_by(owner_permission=owner_permission)
        async with async_session() as session:
            result = await session.execute(query)
            if len(result.scalars().all()) == 1:
                return result.scalars().first()
            return result.scalars().all()

    @log_function_call
    @staticmethod
    async def update_owner(owner_id: int = None,
                           owner_firstname: str = None,
                           owner_surname: str = None,
                           owner_mail: str = None,
                           owner_permission: str = None):
        async with async_session() as session:
            query = select(Owner).filter_by(owner_id=owner_id)
            result = await session.execute(query)
            owner = result.scalars().first()
            if owner_firstname:
                owner.owner_firstname = owner_firstname
            if owner_surname:
                owner.owner_surname = owner_surname
            if owner_mail:
                owner.owner_mail = owner_mail
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
    def get_cat_connection(cat_id: int):
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

    @log_function_call
    @staticmethod
    async def get_user_permission(user_permission_id: int = None,
                                  user_permission_name: str = None,
                                  user_permission_description: str = None):
        query = select(UserPermission)
        if user_permission_id:
            query = query.filter_by(user_permission_id=user_permission_id)
        if user_permission_name:
            query = query.filter_by(user_permission_name=user_permission_name)
        if user_permission_description:
            query = query.filter_by(user_permission_description=user_permission_description)
        async with async_session() as session:
            result = await session.execute(query)
            if len(result.scalars().all()) == 1:
                return result.scalars().first()
            return result.scalars().all()
        
    @log_function_call
    @staticmethod
    async def add_user_permission(user_permission_name: str,
                                  user_permission_description: str):
        async with async_session() as session:
            new_user_permission = UserPermission(
            user_permission_name=user_permission_name, user_permission_description=user_permission_description)
            session.add(new_user_permission)
            await session.commit()
            return new_user_permission
        
    @log_function_call
    @staticmethod
    async def delete_user_permission(user_permission_id: int):
        async with async_session() as session:
            query = select(UserPermission).filter_by(
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
    async def get_country_city(country_id: int = None,
                               country_name: str = None,
                               country_description: str = None):
        query = select(CountryCity)
        if country_id:
            query = query.filter_by(country_id=country_id)
        if country_name:
            query = query.filter_by(country_name=country_name)
        if country_description:
            query = query.filter_by(country_description=country_description)
        async with async_session() as session:
            result = await session.execute(query)
            if len(result.scalars().all()) == 1:
                return result.scalars().first()
            return result.scalars().all()

    @log_function_call
    @staticmethod
    async def add_country_city(country_name: str,
                               country_description: str):
        async with async_session() as session:
            new_country_city = CountryCity(
                country_name=country_name,
                country_description=country_description)
            session.add(new_country_city)
            await session.commit()
            return new_country_city

    @log_function_call
    @staticmethod
    async def delete_country_city(country_id: int):
        async with async_session() as session:
            query = select(CountryCity).filter_by(country_id=country_id)
            result = await session.execute(query)
            country_city = result.scalars().first()
            if country_city:
                await session.delete(country_city)
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
        query = select(User)
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
            query = select(User).filter_by(user_id=user_id)
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
            query = select(User).filter_by(user_id=user_id)
            result = await session.execute(query)
            user = result.scalars().first()
            if user:
                await session.delete(user)
                await session.commit()
                return True
            return False

    @log_function_call
    @staticmethod
    async def get_user_permission(user_permission_id: int = None,
                                  user_permission_name: str = None,
                                  user_permission_description: str = None):
        query = select(UserPermission)
        if user_permission_id:
            query = query.filter_by(user_permission_id=user_permission_id)
        if user_permission_name:
            query = query.filter_by(user_permission_name=user_permission_name)
        if user_permission_description:
            query = query.filter_by(
                user_permission_description=user_permission_description)
        async with async_session() as session:
            result = await session.execute(query)
            if len(result.scalars().all()) == 1:
                return result.scalars().first()
            return result.scalars().all()
        