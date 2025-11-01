from pydantic import BaseModel, Field, field_validator
from typing import List, Optional


# Building
class BuildingBase(BaseModel):
    address: str = Field(..., description="Адрес здания")
    latitude: str = Field(..., description="Широта (строка)")
    longitude: str = Field(..., description="Долгота (строка)")


class BuildingCreate(BuildingBase):
    pass


class BuildingResponse(BuildingBase):
    id: int

    class Config:
        from_attributes = True


# Activity
class ActivityBase(BaseModel):
    name: str = Field(..., description="Название деятельности")
    parent_id: Optional[int] = Field(None, description="ID родительской деятельности")


class ActivityCreate(ActivityBase):
    pass


class ActivityResponse(ActivityBase):
    id: int

    class Config:
        from_attributes = True


# Phone
class PhoneBase(BaseModel):
    number: str = Field(..., description="Номер телефона")


class PhoneCreate(PhoneBase):
    pass


class PhoneResponse(PhoneBase):
    id: int

    class Config:
        from_attributes = True


# Organization
class OrganizationBase(BaseModel):
    name: str = Field(..., description="Название организации")
    phones: List[str] = Field(..., description="Список телефонов организации")


class OrganizationCreate(OrganizationBase):
    building_id: Optional[int] = Field(None, description="ID здания организации")
    activities_ids: List[int] = Field(default_factory=list, description="Список ID видов деятельности")


class OrganizationResponse(BaseModel):
    id: int
    name: str
    phones: List[str]
    building: Optional[BuildingResponse] = None
    activities: List[ActivityResponse] = []

    @field_validator('phones', mode='before')
    @classmethod
    def extract_phone_numbers(cls, v):
        if isinstance(v, list) and len(v) > 0:
            if isinstance(v[0], str):
                return v
            # Если это объекты Phone
            return [phone.number for phone in v]
        return v

    class Config:
        from_attributes = True


class OrganizationListResponse(BaseModel):
    id: int
    name: str
    phones: List[PhoneResponse]

    class Config:
        from_attributes = True
