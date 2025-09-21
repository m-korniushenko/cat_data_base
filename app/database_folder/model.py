from app.database_folder.postgres import Base
from sqlalchemy import (BigInteger, Column, DateTime, ForeignKey,
                        String, UniqueConstraint, func, Date, ARRAY, Boolean, Float, Integer)
from sqlalchemy.orm import relationship

import_model = "Models"


class Owner(Base):
    __tablename__ = 'owner'
    owner_id = Column(BigInteger, primary_key=True, autoincrement=True)
    owner_firstname = Column(String, default=None)
    owner_surname = Column(String, default=None)
    owner_email = Column(String, default=None)
    owner_address = Column(String, nullable=True)
    owner_city = Column(String, nullable=True)
    owner_country = Column(String, nullable=True)
    owner_zip = Column(String, nullable=True)
    owner_birthday = Column(Date, nullable=True)
    owner_phone = Column(String, nullable=True)
    owner_hashed_password = Column(String, nullable=False)
    owner_permission = Column(BigInteger, default=0)


class Cat(Base):
    __tablename__ = 'cat'
    cat_id = Column(BigInteger, primary_key=True, autoincrement=True)
    owner_id = Column(BigInteger)
    cat_breed_id = Column(BigInteger)
    cat_title = Column(ARRAY(String))
    cat_firstname = Column(String)
    cat_surname = Column(String)
    cat_callname = Column(String, nullable=True)
    cat_gender = Column(String)
    cat_birthday = Column(Date)
    cat_dam_id = Column(BigInteger, nullable=True)
    cat_sire_id = Column(BigInteger, nullable=True)
    cat_microchip_number = Column(String, nullable=True)
    cat_EMS_colour = Column(String, nullable=True)
    cat_litter = Column(String, nullable=True)
    cat_haritage_number = Column(String, nullable=True)
    cat_haritage_number_2 = Column(String, nullable=True)
    cat_eye_colour = Column(String, nullable=True)
    cat_hair_type = Column(String, nullable=True)
    cat_tests = Column(String, nullable=True)
    cat_litter_size_male = Column(Integer, nullable=True)
    cat_litter_size_female = Column(Integer, nullable=True)
    cat_blood_group = Column(String, nullable=True)
    cat_gencode = Column(String, nullable=True)
    cat_features = Column(String, nullable=True)
    cat_notes = Column(String, nullable=True)
    cat_show_results = Column(String, nullable=True)
    cat_breeding_lock = Column(Boolean, default=False)
    cat_breeding_lock_date = Column(Date, nullable=True)
    cat_breeding_animal = Column(Boolean, default=False)
    cat_birth_country = Column(String, nullable=True)
    cat_location = Column(String, nullable=True)
    cat_weight = Column(Float, nullable=True)
    cat_birth_weight = Column(Float, nullable=True)
    cat_transfer_weight = Column(Float, nullable=True)
    cat_faults_deviations = Column(String, nullable=True)
    cat_association = Column(String, nullable=True)
    cat_jaw_fault = Column(String, nullable=True)
    cat_hernia = Column(String, nullable=True)
    cat_testicles = Column(String, nullable=True)
    cat_death_date = Column(Date, nullable=True)
    cat_death_cause = Column(String, nullable=True)
    cat_status = Column(String, nullable=True)
    cat_kitten_transfer = Column(Boolean, default=False)
    cat_description = Column(String, nullable=True)
    cat_photos = Column(ARRAY(String))
    cat_files = Column(ARRAY(String))
    wcf_sticker = Column(String, nullable=True)


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
    breed_gender = Column(String, nullable=True)
    breed_birthday = Column(Date, nullable=True)
    breed_address = Column(String, nullable=True)
    breed_city = Column(String, nullable=True)
    breed_country = Column(String, nullable=True)
    breed_zip = Column(String, nullable=True)
    breed_phone = Column(String, nullable=True)
    breed_email = Column(String)
    breed_description = Column(String, nullable=True)
