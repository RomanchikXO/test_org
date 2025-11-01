import requests
import json

BASE_URL = "http://localhost:8000"
API_KEY = "fastapi+pydantic+sqlalchemy+alembic"
HEADERS = {"X-API-Key": API_KEY, "Content-Type": "application/json"}


def pretty(data):
    print(json.dumps(data, ensure_ascii=False, indent=2))


# Создание здания
def test_create_building():
    payload = {
        "address": "г. Москва, ул. Ленина 1, офис 3",
        "latitude": "55.7558",
        "longitude": "37.6173"
    }
    r = requests.post(f"{BASE_URL}/buildings/", headers=HEADERS, json=payload)
    print("Создание здания:", r.status_code)
    pretty(r.json())
    return r.json()["id"]


# Создание деятельности
def test_create_activity(name, parent_id=None):
    payload = {"name": name}
    if parent_id:
        payload["parent_id"] = parent_id
    r = requests.post(f"{BASE_URL}/activities/", headers=HEADERS, json=payload)
    print(f"Создание деятельности '{name}':", r.status_code)
    pretty(r.json())
    return r.json()["id"]


# Создание организации
def test_create_organization(building_id, activity_ids):
    payload = {
        "name": "ООО РомТех",
        "phones": ["2-222-222", "8-923-666-13-13"],
        "building_id": building_id,
        "activities_ids": activity_ids
    }
    r = requests.post(f"{BASE_URL}/organizations/", headers=HEADERS, json=payload)
    print("Создание организации:", r.status_code)
    pretty(r.json())
    return r.json()["id"]


# Получить организацию по ID
def test_get_organization(org_id):
    r = requests.get(f"{BASE_URL}/organizations/{org_id}", headers=HEADERS)
    print(f"Получение организации {org_id}:", r.status_code)
    pretty(r.json())


# Список всех организаций
def test_list_organizations():
    r = requests.get(f"{BASE_URL}/organizations/", headers=HEADERS)
    print("Список организаций:", r.status_code)
    pretty(r.json())


# Поиск организаций по названию
def test_search_organizations(name):
    r = requests.get(f"{BASE_URL}/organizations/search/", headers=HEADERS, params={"name": name})
    print(f"Поиск организаций по имени '{name}':", r.status_code)
    pretty(r.json())


# Список организаций в здании
def test_organizations_in_building(building_id):
    r = requests.get(f"{BASE_URL}/buildings/{building_id}/organizations/", headers=HEADERS)
    print(f"Организации в здании {building_id}:", r.status_code)
    pretty(r.json())


# Список организаций по деятельности
def test_organizations_by_activity(activity_id):
    r = requests.get(f"{BASE_URL}/activities/{activity_id}/organizations/", headers=HEADERS)
    print(f"Организации по деятельности {activity_id}:", r.status_code)
    pretty(r.json())


# Организации рядом (по координатам)
def test_organizations_nearby(lat, lon, radius):
    params = {"latitude": lat, "longitude": lon, "radius_m": radius}
    r = requests.get(f"{BASE_URL}/organizations/nearby/", headers=HEADERS, params=params)
    print(f"Организации рядом с ({lat},{lon}) радиус {radius}м:", r.status_code)
    pretty(r.json())


if __name__ == "__main__":
    # Создаем здание
    building_id = test_create_building()

    # Создаем дерево видов деятельности
    food_id = test_create_activity("Еда")
    meat_id = test_create_activity("Мясная продукция", parent_id=food_id)
    milk_id = test_create_activity("Молочная продукция", parent_id=food_id)
    auto_id = test_create_activity("Автомобили")
    trucks_id = test_create_activity("Грузовые", parent_id=auto_id)

    # Создаем организацию
    org_id = test_create_organization(building_id, activity_ids=[meat_id, milk_id])

    # Получаем организацию по ID
    test_get_organization(org_id)

    # Список всех организаций
    test_list_organizations()

    # Поиск по названию
    test_search_organizations("РомТех")

    # Организации в здании
    test_organizations_in_building(building_id)

    # Организации по деятельности "Еда" (включая вложенные)
    test_organizations_by_activity(food_id)

    # Организации рядом с координатами
    test_organizations_nearby(55.7555, 37.6174, 2000)
