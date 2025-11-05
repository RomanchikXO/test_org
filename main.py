import os
from dotenv import load_dotenv
from fastapi import FastAPI, Depends, HTTPException, status, Security, Query
from fastapi.security import APIKeyHeader
from sqlalchemy.orm import Session
from typing import List
import math

from database import engine, get_db
from models import Base, Organization, Building, Activity, Phone
from schemas import (
    OrganizationCreate, OrganizationResponse, OrganizationListResponse,
    BuildingCreate, BuildingResponse,
    ActivityCreate, ActivityResponse
)

load_dotenv()

# Создание таблиц
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Organization Management API",
    description="REST API для управления организациями, зданиями и видами деятельности",
    version="1.0.0"
)

API_KEY = os.getenv("API_KEY")
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=True)


def verify_api_key(api_key: str = Security(api_key_header)):
    if api_key != API_KEY:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Неверный API ключ"
        )
    return api_key


# CRUD Organizations

@app.post("/organizations/", response_model=OrganizationResponse, status_code=status.HTTP_201_CREATED)
def create_organization(org: OrganizationCreate, db: Session = Depends(get_db), api_key: str = Depends(verify_api_key)):
    db_org = Organization(name=org.name, building_id=org.building_id)
    db.add(db_org)
    db.commit()
    db.refresh(db_org)

    # Добавляем телефоны
    for number in org.phones:
        phone = Phone(number=number, organization_id=db_org.id)
        db.add(phone)
    db.commit()

    # Привязка видов деятельности
    if org.activities_ids:
        activities = db.query(Activity).filter(Activity.id.in_(org.activities_ids)).all()
        db_org.activities = activities
        db.commit()
        db.refresh(db_org)

    return db_org


@app.get("/organizations/{org_id}", response_model=OrganizationResponse)
def get_organization(org_id: int, db: Session = Depends(get_db), api_key: str = Depends(verify_api_key)):
    org = db.query(Organization).filter(Organization.id == org_id).first()
    if not org:
        raise HTTPException(404, "Организация не найдена")
    return org


@app.get("/organizations/", response_model=List[OrganizationListResponse])
def list_organizations(db: Session = Depends(get_db), api_key: str = Depends(verify_api_key)):
    return db.query(Organization).all()


@app.get("/organizations/search/", response_model=List[OrganizationResponse])
def search_organizations(name: str, db: Session = Depends(get_db), api_key: str = Depends(verify_api_key)):
    return db.query(Organization).filter(Organization.name.ilike(f"%{name}%")).all()


# CRUD Buildings

@app.post("/buildings/", response_model=BuildingResponse, status_code=status.HTTP_201_CREATED)
def create_building(building: BuildingCreate, db: Session = Depends(get_db), api_key: str = Depends(verify_api_key)):
    db_building = Building(**building.model_dump())
    db.add(db_building)
    db.commit()
    db.refresh(db_building)
    return db_building


@app.get("/buildings/{building_id}/organizations/", response_model=List[OrganizationResponse])
def organizations_in_building(building_id: int, db: Session = Depends(get_db), api_key: str = Depends(verify_api_key)):
    building = db.query(Building).filter(Building.id == building_id).first()
    if not building:
        raise HTTPException(404, "Здание не найдено")
    orgs = db.query(Organization).filter(Organization.building_id == building.id).all()
    return orgs


# CRUD Activities

@app.post("/activities/", response_model=ActivityResponse, status_code=status.HTTP_201_CREATED)
def create_activity(activity: ActivityCreate, db: Session = Depends(get_db), api_key: str = Depends(verify_api_key)):
    # Проверка на существование деятельности с таким именем
    existing = db.query(Activity).filter(Activity.name == activity.name).first()
    if existing:
        raise HTTPException(400, f"Деятельность с названием '{activity.name}' уже существует")

    # Проверка вложенности (максимум 3 уровня)
    level = 1
    parent_id = activity.parent_id
    while parent_id:
        parent = db.query(Activity).filter(Activity.id == parent_id).first()
        if not parent:
            raise HTTPException(404, "Родительская деятельность не найдена")
        parent_id = parent.parent_id
        level += 1
        if level > 3:
            raise HTTPException(400, "Превышен уровень вложенности (максимум 3)")

    db_activity = Activity(**activity.model_dump())
    db.add(db_activity)
    db.commit()
    db.refresh(db_activity)
    return db_activity


@app.get("/activities/{activity_id}/organizations/", response_model=List[OrganizationResponse])
def organizations_by_activity(activity_id: int, db: Session = Depends(get_db), api_key: str = Depends(verify_api_key)):
    # Рекурсивно собираем id всех дочерних видов (до 3 уровней)
    def collect_ids(act_id, level=1):
        if level > 3:
            return []
        children = db.query(Activity).filter(Activity.parent_id == act_id).all()
        ids = [c.id for c in children]
        for c in children:
            ids.extend(collect_ids(c.id, level + 1))
        return ids

    activity = db.query(Activity).filter(Activity.id == activity_id).first()
    if not activity:
        raise HTTPException(404, "Вид деятельности не найден")

    all_ids = [activity.id] + collect_ids(activity.id)
    orgs = db.query(Organization).join(Organization.activities).filter(Activity.id.in_(all_ids)).all()
    return orgs


# Organizations Nearby

@app.get("/organizations/nearby/", response_model=List[OrganizationResponse])
def organizations_nearby(
    latitude: float = Query(...),
    longitude: float = Query(...),
    radius_m: float = Query(1000),
    db: Session = Depends(get_db),
    api_key: str = Depends(verify_api_key)
):
    def haversine(lat1, lon1, lat2, lon2):
        R = 6371000
        phi1, phi2 = math.radians(lat1), math.radians(lat2)
        dphi, dlambda = math.radians(lat2 - lat1), math.radians(lon2 - lon1)
        a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2)**2
        return 2*R*math.atan2(math.sqrt(a), math.sqrt(1-a))

    organizations = db.query(Organization).join(Building).all()
    nearby = []
    for org in organizations:
        if not org.building:
            continue
        lat, lon = float(org.building.latitude), float(org.building.longitude)
        distance = haversine(latitude, longitude, lat, lon)
        if distance <= radius_m:
            nearby.append(org)
    return nearby
