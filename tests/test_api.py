"""Tests for the Smart Expense Tracker API."""
import pytest

from src.app import create_app


@pytest.fixture
def client():
    app = create_app(persist_path=None)  # in-memory only, no data.json during tests
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def add_sample_expense(client, title="Lunch", amount=12.5, category="Food", date="2026-01-15"):
    return client.post("/expenses", json={
        "title": title, "amount": amount, "category": category, "date": date,
    })


def test_health_check(client):
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.get_json() == {"status": "ok"}


def test_add_expense_success(client):
    resp = add_sample_expense(client)
    assert resp.status_code == 201
    data = resp.get_json()
    assert data["title"] == "Lunch"
    assert data["amount"] == 12.5
    assert data["category"] == "Food"
    assert data["date"] == "2026-01-15"
    assert "id" in data


@pytest.mark.parametrize("field,value,message_snippet", [
    ("title", "", "title"),
    ("amount", -5, "amount"),
    ("amount", "abc", "amount"),
    ("category", "", "category"),
    ("date", "15-01-2026", "date"),
])
def test_add_expense_validation_errors(client, field, value, message_snippet):
    payload = {"title": "Lunch", "amount": 12.5, "category": "Food", "date": "2026-01-15"}
    payload[field] = value
    resp = client.post("/expenses", json=payload)
    assert resp.status_code == 400
    assert message_snippet in resp.get_json()["error"]


def test_add_expense_missing_body(client):
    resp = client.post("/expenses")
    assert resp.status_code == 400


def test_list_expenses_empty(client):
    resp = client.get("/expenses")
    assert resp.status_code == 200
    assert resp.get_json() == []


def test_list_expenses(client):
    add_sample_expense(client, title="Lunch", category="Food")
    add_sample_expense(client, title="Bus ticket", category="Transport", amount=3.0)
    resp = client.get("/expenses")
    assert resp.status_code == 200
    assert len(resp.get_json()) == 2


def test_filter_by_category_case_insensitive(client):
    add_sample_expense(client, title="Lunch", category="Food")
    add_sample_expense(client, title="Bus ticket", category="Transport", amount=3.0)
    resp = client.get("/expenses?category=food")
    data = resp.get_json()
    assert len(data) == 1
    assert data[0]["title"] == "Lunch"


def test_total_overall_and_by_category(client):
    add_sample_expense(client, category="Food", amount=10)
    add_sample_expense(client, category="Food", amount=15.5)
    resp = client.get("/expenses/summary")
    data = resp.get_json()
    assert data["total"] == 25.5
    assert data["by_category"]["Food"] == 25.5


def test_total_for_specific_category(client):
    add_sample_expense(client, category="Food", amount=10)
    add_sample_expense(client, category="Transport", amount=5)
    resp = client.get("/expenses/summary?category=Transport")
    data = resp.get_json()
    assert data["category"] == "Transport"
    assert data["total"] == 5


def test_get_single_expense(client):
    created = add_sample_expense(client).get_json()
    resp = client.get(f"/expenses/{created['id']}")
    assert resp.status_code == 200
    assert resp.get_json()["id"] == created["id"]


def test_get_single_expense_not_found(client):
    resp = client.get("/expenses/does-not-exist")
    assert resp.status_code == 404


def test_delete_expense(client):
    created = add_sample_expense(client).get_json()
    resp = client.delete(f"/expenses/{created['id']}")
    assert resp.status_code == 204
    resp = client.get(f"/expenses/{created['id']}")
    assert resp.status_code == 404


def test_delete_nonexistent_expense(client):
    resp = client.delete("/expenses/does-not-exist")
    assert resp.status_code == 404


def test_search_expenses(client):
    add_sample_expense(client, title="Grocery run", category="Food")
    add_sample_expense(client, title="Bus ticket", category="Transport", amount=3.0)
    resp = client.get("/expenses/search?q=grocery")
    data = resp.get_json()
    assert len(data) == 1
    assert data[0]["title"] == "Grocery run"


def test_search_expenses_missing_query(client):
    resp = client.get("/expenses/search")
    assert resp.status_code == 400
