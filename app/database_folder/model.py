from app.database_folder.postgres import Base
from sqlalchemy import (BigInteger, Column, DateTime, ForeignKey,
                        String, UniqueConstraint, func)
from sqlalchemy.orm import relationship


import_model = "Models"


class Owner(Base):
    __tablename__ = 'owner'
    owner_id = Column(BigInteger, primary_key=True, autoincrement=True)
    owner_firstname = Column(String, default=None)
    owner_surname = Column(String, default=None)
    owner_mail = Column(String, default=None)
    owner_permission = Column(BigInteger, default=0)


class Cat(Base):
    __tablename__ = 'cat'
    cat_id = Column(BigInteger, primary_key=True, autoincrement=True)
    owner_id = Column(BigInteger, ForeignKey('owner.owner_id'))
    cat_firstname = Column(String)
    cat_surname = Column(String, default="ordinary")
    cat_gender = Column(String)
    cat_birthday = Column(DateTime)
    cat_microchip_number = Column(String)
    cat_breed = Column(String)
    cat_colour = Column(String)
    cat_litter = Column(String)
    cat_ifc = Column(String)


class History(Base):
    __tablename__ = 'history'
    history_id = Column(BigInteger, primary_key=True, autoincrement=True)
    history_time = Column(DateTime, default=func.now())
    cat_id = Column(BigInteger)
    user_id = Column(BigInteger)
    history_action = Column(String)


class CatConnection(Base):
    __tablename__ = 'cat_connection'
    connection_id = Column(BigInteger, primary_key=True, autoincrement=True)
    cat_father_id = Column(BigInteger)
    cat_mother_id = Column(BigInteger)


class CatType(Base):
    __tablename__ = 'cat_type'
    cat_type_id = Column(BigInteger, primary_key=True, autoincrement=True)
    cat_type_name = Column(String, unique=True)
    cat_type_description = Column(String, default=None)


class UserPermission(Base):
    __tablename__ = 'user_permission'
    user_permission_id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_permission_name = Column(String, unique=True)
    user_permission_description = Column(String, default=None)


class CountryCity(Base):
    __tablename__ = 'country_city'
    country_id = Column(BigInteger, primary_key=True, autoincrement=True)
    country_name = Column(String, unique=True)
    country_description = Column(String, default=None)
