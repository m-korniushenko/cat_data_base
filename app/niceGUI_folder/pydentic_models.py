from pydantic import BaseModel
from typing import Optional
from datetime import datetime, date


class CatCreate(BaseModel):
    owner_id: int
    cat_firstname: str
    cat_surname: str = "ordinary"
    cat_gender: str
    cat_birthday: datetime
    cat_microchip_number: str
    cat_breed_id: str
    cat_EMS_colour: str
    cat_litter: str

    class Config:
        from_attributes = True


class CatUpdate(BaseModel):
    owner_id: Optional[int] = None
    cat_firstname: Optional[str] = None
    cat_surname: Optional[str] = None
    cat_gender: Optional[str] = None
    cat_birthday: Optional[datetime] = None
    cat_microchip_number: Optional[str] = None
    cat_breed_id: Optional[str] = None
    cat_EMS_colour: Optional[str] = None
    cat_litter: Optional[str] = None

    class Config:
        from_attributes = True


class OwnerCreate(BaseModel):
    owner_firstname: str
    owner_surname: str
    owner_email: str
    owner_address: Optional[str] = None
    owner_city: Optional[str] = None
    owner_country: Optional[str] = None
    owner_zip: Optional[str] = None
    owner_birthday: Optional[date] = None
    owner_phone: Optional[str] = None
    owner_hashed_password: str
    owner_permission: int = 0

    class Config:
        from_attributes = True


class OwnerUpdate(BaseModel):
    owner_firstname: Optional[str] = None
    owner_surname: Optional[str] = None
    owner_email: Optional[str] = None
    owner_address: Optional[str] = None
    owner_city: Optional[str] = None
    owner_country: Optional[str] = None
    owner_zip: Optional[str] = None
    owner_birthday: Optional[date] = None
    owner_phone: Optional[str] = None
    owner_hashed_password: Optional[str] = None
    owner_permission: Optional[int] = None

    class Config:
        from_attributes = True


class BreedCreate(BaseModel):
    breed_firstname: str
    breed_surname: str
    breed_gender: Optional[str] = None
    breed_birthday: Optional[date] = None
    breed_address: Optional[str] = None
    breed_city: Optional[str] = None
    breed_country: Optional[str] = None
    breed_zip: Optional[str] = None
    breed_phone: Optional[str] = None
    breed_email: str
    breed_description: Optional[str] = None

    class Config:
        from_attributes = True


class BreedUpdate(BaseModel):
    breed_firstname: Optional[str] = None
    breed_surname: Optional[str] = None
    breed_gender: Optional[str] = None
    breed_birthday: Optional[date] = None
    breed_address: Optional[str] = None
    breed_city: Optional[str] = None
    breed_country: Optional[str] = None
    breed_zip: Optional[str] = None
    breed_phone: Optional[str] = None
    breed_email: Optional[str] = None
    breed_description: Optional[str] = None

    class Config:
        from_attributes = True