from app.database_folder.postgres import Base
from sqlalchemy import (BigInteger, Column, DateTime, ForeignKey,
                        String, UniqueConstraint, func, Date, ARRAY)
from sqlalchemy.orm import relationship

import_model = "Models"


class Owner(Base):
    __tablename__ = 'owner'
    owner_id = Column(BigInteger, primary_key=True, autoincrement=True)
    owner_firstname = Column(String, default=None)
    owner_surname = Column(String, default=None)
    owner_mail = Column(String, default=None)
    owner_hashed_password = Column(String, nullable=False)
    owner_permission = Column(BigInteger, default=0)


class Cat(Base):
    __tablename__ = 'cat'
    cat_id = Column(BigInteger, primary_key=True, autoincrement=True)
    owner_id = Column(BigInteger)
    cat_breed_id = Column(BigInteger) #breed - это развадитель котов
    cat_title = Column(ARRAY(String))
    cat_firstname = Column(String)
    cat_surname = Column(String)
    cat_gender = Column(String)
    cat_birthday = Column(Date)
    cat_dam_id = Column(BigInteger, nullable=True)
    cat_sire_id = Column(BigInteger, nullable=True)
    cat_microchip_number = Column(String)
    cat_EMS_colour = Column(String)
    cat_litter = Column(String)
    cat_haritage_number = Column(String)
    cat_description = Column(String)
    cat_photos = Column(ARRAY(String))
    cat_files = Column(ARRAY(String))


class History(Base):
    __tablename__ = 'history'
    history_id = Column(BigInteger, primary_key=True, autoincrement=True)
    history_time = Column(DateTime, default=func.now())
    cat_id = Column(BigInteger)
    user_id = Column(BigInteger)
    history_action = Column(String)


class OwnerPermission(Base):
    __tablename__ = 'owner_permission'
    owner_permission_id = Column(BigInteger, primary_key=True, autoincrement=True)
    owner_permission_name = Column(String, unique=True)
    owner_permission_description = Column(String, default=None)


class Breed(Base):
    __tablename__ = 'breed'
    breed_id = Column(BigInteger, primary_key=True, autoincrement=True)
    breed_firstname = Column(String)
    breed_surname = Column(String)
    breed_email = Column(String)
    breed_description = Column(String, default=None)
