from uuid import uuid4

import pytest
from faker import Faker
from httpx import AsyncClient

fake = Faker()


@pytest.mark.asyncio(loop_scope="session")
async def test_create_product_with_all_fields(async_client: AsyncClient):
    payload = {
        "name": fake.unique.word(),
        "description": fake.text(),
        "price": 1999.99,
        "category": "Electronics",
    }

    response = await async_client.post("/api/v1/products/", json=payload)

    assert response.status_code == 200
    data = response.json()

    assert data["name"] == payload["name"]
    assert data["description"] == payload["description"]
    assert data["price"] == payload["price"]
    assert data["image"] is None
    assert data["category"] == payload["category"]
    assert "id" in data


@pytest.mark.asyncio(loop_scope="session")
async def test_create_product_with_required_fields_only(async_client: AsyncClient):
    payload = {
        "name": fake.unique.word(),
        "price": 500,
        "category": "Books",
    }

    response = await async_client.post("/api/v1/products/", json=payload)

    assert response.status_code == 200
    data = response.json()

    assert data["name"] == payload["name"]
    assert data["price"] == payload["price"]
    assert data["category"] == payload["category"]
    assert data["description"] is None
    assert data["image"] is None


@pytest.mark.asyncio(loop_scope="session")
async def test_create_product_with_minimal_price(async_client: AsyncClient):
    payload = {
        "name": fake.unique.word(),
        "price": 1,
        "category": "Free",
    }

    response = await async_client.post("/api/v1/products/", json=payload)

    assert response.status_code == 200
    data = response.json()

    assert data["price"] == 1


@pytest.mark.asyncio(loop_scope="session")
async def test_create_product_with_decimal_price(async_client: AsyncClient):
    payload = {
        "name": fake.unique.word(),
        "price": 1234.56,
        "category": "Finance",
    }

    response = await async_client.post("/api/v1/products/", json=payload)

    assert response.status_code == 200
    data = response.json()

    assert float(data["price"]) == 1234.56


@pytest.mark.asyncio(loop_scope="session")
async def test_bulk_create_products(async_client: AsyncClient):
    products = [
        {
            "name": fake.unique.word(),
            "price": 100,
            "category": "Test",
        }
        for _ in range(3)
    ]

    response = await async_client.post("/api/v1/products/bulk", json=products)
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3
    for i, product in enumerate(products):
        assert data[i]["name"] == product["name"]


@pytest.mark.asyncio(loop_scope="session")
async def test_get_product_by_valid_uuid(async_client: AsyncClient):
    payload = {
        "name": fake.unique.word(),
        "price": 500,
        "category": "Test",
    }
    create_resp = await async_client.post("/api/v1/products/", json=payload)
    assert create_resp.status_code == 200
    product_id = create_resp.json()["id"]

    get_resp = await async_client.get(f"/api/v1/products/{product_id}")
    assert get_resp.status_code == 200
    data = get_resp.json()
    assert data["id"] == product_id
    assert data["name"] == payload["name"]


@pytest.mark.asyncio(loop_scope="session")
async def test_cant_create_product_with_duplicate_name(async_client: AsyncClient):
    name = "DuplicateProduct"

    payload = {
        "name": name,
        "price": 1000,
        "category": "Test",
    }

    response1 = await async_client.post("/api/v1/products/", json=payload)
    assert response1.status_code == 200

    response2 = await async_client.post("/api/v1/products/", json=payload)
    assert response2.status_code == 409
    data = response2.json()
    assert "A product with this name already exists".lower() in data["detail"].lower()


@pytest.mark.asyncio(loop_scope="session")
async def test_cant_create_product_with_zero_price(async_client: AsyncClient):
    payload = {
        "name": fake.unique.word(),
        "price": 0,
        "category": "Free",
    }

    response = await async_client.post("/api/v1/products/", json=payload)

    assert response.status_code == 422


@pytest.mark.asyncio(loop_scope="session")
async def test_cant_create_product_with_price_overflow(async_client: AsyncClient):
    payload = {
        "name": "ExpensiveProduct",
        "price": 1234567890100.23,  # > DECIMAL(12,2)
        "category": "Test",
    }

    response = await async_client.post("/api/v1/products/", json=payload)
    assert response.status_code == 400
    data = response.json()
    assert "there was an issue processing the statement." in data["detail"].lower()


@pytest.mark.asyncio(loop_scope="session")
async def test_cant_bulk_create_products_with_duplicate_name(async_client: AsyncClient):
    duplicate_name = fake.unique.word()
    products = [
        {"name": duplicate_name, "price": 100, "category": "Test"},
        {"name": duplicate_name, "price": 200, "category": "Test"},
    ]

    response = await async_client.post("/api/v1/products/bulk", json=products)
    assert response.status_code == 409
    data = response.json()
    assert "A product with this name already exists".lower() in data["detail"].lower()


@pytest.mark.asyncio(loop_scope="session")
async def test_cant_get_product_with_nonexistent_uuid(async_client: AsyncClient):
    non_existent_uuid = str(uuid4())
    response = await async_client.get(f"/api/v1/products/{non_existent_uuid}")
    assert response.status_code == 404
    data = response.json()
    assert "not found" in data["detail"].lower()


@pytest.mark.asyncio
async def test_cant_get_product_with_invalid_uuid(async_client: AsyncClient):
    invalid_uuid = "123-invalid-uuid"
    response = await async_client.get(f"/api/v1/products/{invalid_uuid}")
    assert response.status_code == 422
