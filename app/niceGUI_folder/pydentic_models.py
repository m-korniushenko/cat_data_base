from pydantic import BaseModel
from typing import Optional
from datetime import datetime


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
        orm_mode = True


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
        orm_mode = True


class OwnerCreate(BaseModel):
    owner_firstname: str
    owner_surname: str
    owner_mail: str
    owner_hashed_password: str
    owner_permission: str

    class Config:
        orm_mode = True


class OwnerUpdate(BaseModel):
    owner_firstname: Optional[str] = None
    owner_surname: Optional[str] = None
    owner_mail: Optional[str] = None
    owner_hashed_password: Optional[str] = None
    owner_permission: Optional[str] = None

    class Config:
        orm_mode = True