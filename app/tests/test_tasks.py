import asyncio
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from fastapi.testclient import TestClient
from bson import ObjectId
from datetime import datetime, timezone


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def make_task_doc(title="Clean room", points=10, assigned_to="member1", completed=False):
    oid = ObjectId()
    return {
        "_id": oid,
        "title": title,
        "description": None,
        "points": points,
        "assigned_to": assigned_to,
        "completed": completed,
        "created_at": datetime.now(timezone.utc),
    }


def make_transaction_doc(member_id="member1", points=10, type_="earned", ref_id="ref1"):
    return {
        "_id": ObjectId(),
        "member_id": member_id,
        "points": points,
        "type": type_,
        "reference_id": ref_id,
        "created_at": datetime.now(timezone.utc),
    }


def make_reward_doc(name="Ice cream", cost=50):
    return {
        "_id": ObjectId(),
        "name": name,
        "description": None,
        "cost": cost,
    }


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def mock_db():
    return MagicMock()


@pytest.fixture
def client(mock_db):
    with patch("app.db.mongodb.connect_to_mongo", new_callable=AsyncMock), \
         patch("app.db.mongodb.close_mongo_connection", new_callable=AsyncMock):
        from app.main import app
        from app.db.mongodb import get_db
        app.dependency_overrides[get_db] = lambda: mock_db
        with TestClient(app) as c:
            yield c
        app.dependency_overrides.clear()


# ---------------------------------------------------------------------------
# Root
# ---------------------------------------------------------------------------

def test_root(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "StarLance API"}


# ---------------------------------------------------------------------------
# Tasks
# ---------------------------------------------------------------------------

def test_create_task(client, mock_db):
    oid = ObjectId()
    mock_db.tasks.insert_one = AsyncMock(return_value=MagicMock(inserted_id=oid))

    response = client.post("/tasks/", json={
        "title": "Clean room",
        "points": 10,
        "assigned_to": "member1",
    })

    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Clean room"
    assert data["points"] == 10
    assert data["id"] == str(oid)


def test_get_tasks_empty(client, mock_db):
    mock_db.tasks.find.return_value.to_list = AsyncMock(return_value=[])

    response = client.get("/tasks/")
    assert response.status_code == 200
    assert response.json() == []


def test_get_tasks(client, mock_db):
    task_doc = make_task_doc()
    mock_db.tasks.find.return_value.to_list = AsyncMock(return_value=[task_doc])

    response = client.get("/tasks/")
    assert response.status_code == 200
    tasks = response.json()
    assert len(tasks) == 1
    assert tasks[0]["title"] == "Clean room"


def test_get_task_found(client, mock_db):
    task_doc = make_task_doc()
    mock_db.tasks.find_one = AsyncMock(return_value=task_doc)

    response = client.get(f"/tasks/{task_doc['_id']}")
    assert response.status_code == 200
    assert response.json()["title"] == "Clean room"


def test_get_task_not_found(client, mock_db):
    mock_db.tasks.find_one = AsyncMock(return_value=None)

    response = client.get(f"/tasks/{ObjectId()}")
    assert response.status_code == 404


def test_update_task(client, mock_db):
    task_doc = make_task_doc()
    task_id = str(task_doc["_id"])
    updated_doc = {**task_doc, "title": "Updated room"}

    mock_db.tasks.update_one = AsyncMock()
    mock_db.tasks.find_one = AsyncMock(return_value=updated_doc)

    response = client.put(f"/tasks/{task_id}", json={"title": "Updated room"})
    assert response.status_code == 200
    assert response.json()["title"] == "Updated room"


def test_complete_task(client, mock_db):
    task_doc = make_task_doc()
    task_id = str(task_doc["_id"])
    completed_doc = {**task_doc, "_id": task_doc["_id"], "completed": True}

    mock_db.tasks.find_one = AsyncMock(side_effect=[task_doc, completed_doc])
    mock_db.tasks.update_one = AsyncMock()
    mock_db.transactions.insert_one = AsyncMock(
        return_value=MagicMock(inserted_id=ObjectId())
    )

    response = client.post(f"/tasks/{task_id}/complete")
    assert response.status_code == 200
    assert response.json()["completed"] is True


def test_complete_task_not_found(client, mock_db):
    mock_db.tasks.find_one = AsyncMock(return_value=None)

    response = client.post(f"/tasks/{ObjectId()}/complete")
    assert response.status_code == 404


def test_complete_task_already_completed(client, mock_db):
    task_doc = make_task_doc(completed=True)
    mock_db.tasks.find_one = AsyncMock(return_value=task_doc)

    response = client.post(f"/tasks/{task_doc['_id']}/complete")
    assert response.status_code == 400


# ---------------------------------------------------------------------------
# Balance
# ---------------------------------------------------------------------------

def test_get_balance(client, mock_db):
    transactions = [
        make_transaction_doc(points=10, type_="earned"),
        make_transaction_doc(points=3, type_="spent"),
    ]
    mock_db.transactions.find.return_value.to_list = AsyncMock(return_value=transactions)

    response = client.get("/balance/member1")
    assert response.status_code == 200
    data = response.json()
    assert data["balance"] == 7
    assert data["member_id"] == "member1"


def test_get_balance_empty(client, mock_db):
    mock_db.transactions.find.return_value.to_list = AsyncMock(return_value=[])

    response = client.get("/balance/member1")
    assert response.status_code == 200
    assert response.json()["balance"] == 0


def test_get_transactions(client, mock_db):
    transaction = make_transaction_doc()
    mock_db.transactions.find.return_value.to_list = AsyncMock(return_value=[transaction])

    response = client.get("/balance/member1/transactions")
    assert response.status_code == 200
    assert len(response.json()) == 1


# ---------------------------------------------------------------------------
# Rewards
# ---------------------------------------------------------------------------

def test_create_reward(client, mock_db):
    oid = ObjectId()
    mock_db.rewards.insert_one = AsyncMock(return_value=MagicMock(inserted_id=oid))

    response = client.post("/rewards/", json={"name": "Ice cream", "cost": 50})
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Ice cream"
    assert data["id"] == str(oid)


def test_get_rewards_empty(client, mock_db):
    mock_db.rewards.find.return_value.to_list = AsyncMock(return_value=[])

    response = client.get("/rewards/")
    assert response.status_code == 200
    assert response.json() == []


def test_get_rewards(client, mock_db):
    reward_doc = make_reward_doc()
    mock_db.rewards.find.return_value.to_list = AsyncMock(return_value=[reward_doc])

    response = client.get("/rewards/")
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_redeem_reward_success(client, mock_db):
    reward_doc = make_reward_doc(cost=50)
    reward_id = str(reward_doc["_id"])
    transactions = [make_transaction_doc(points=100, type_="earned")]

    mock_db.rewards.find_one = AsyncMock(return_value=reward_doc)
    mock_db.transactions.find.return_value.to_list = AsyncMock(return_value=transactions)
    mock_db.transactions.insert_one = AsyncMock(
        return_value=MagicMock(inserted_id=ObjectId())
    )

    response = client.post(f"/rewards/{reward_id}/redeem/member1")
    assert response.status_code == 200
    data = response.json()
    assert "reward" in data
    assert "transaction" in data


def test_redeem_reward_not_found(client, mock_db):
    mock_db.rewards.find_one = AsyncMock(return_value=None)

    response = client.post(f"/rewards/{ObjectId()}/redeem/member1")
    assert response.status_code == 404


def test_redeem_reward_insufficient_balance(client, mock_db):
    reward_doc = make_reward_doc(cost=100)
    reward_id = str(reward_doc["_id"])
    transactions = [make_transaction_doc(points=50, type_="earned")]

    mock_db.rewards.find_one = AsyncMock(return_value=reward_doc)
    mock_db.transactions.find.return_value.to_list = AsyncMock(return_value=transactions)

    response = client.post(f"/rewards/{reward_id}/redeem/member1")
    assert response.status_code == 400


# ---------------------------------------------------------------------------
# Family repository (direct async tests)
# ---------------------------------------------------------------------------

def test_family_create_member():
    from app.repositories.family_repository import create_member
    db = MagicMock()
    oid = ObjectId()
    db.members.insert_one = AsyncMock(return_value=MagicMock(inserted_id=oid))

    result = asyncio.run(create_member(db, {"name": "Alice", "role": "parent"}))
    assert result["id"] == str(oid)
    assert result["name"] == "Alice"


def test_family_get_member_found():
    from app.repositories.family_repository import get_member
    db = MagicMock()
    oid = ObjectId()
    db.members.find_one = AsyncMock(return_value={"_id": oid, "name": "Alice"})

    result = asyncio.run(get_member(db, str(oid)))
    assert result["name"] == "Alice"
    assert result["id"] == str(oid)


def test_family_get_member_not_found():
    from app.repositories.family_repository import get_member
    db = MagicMock()
    db.members.find_one = AsyncMock(return_value=None)

    result = asyncio.run(get_member(db, str(ObjectId())))
    assert result is None


def test_family_get_members():
    from app.repositories.family_repository import get_members
    db = MagicMock()
    oid = ObjectId()
    db.members.find.return_value.to_list = AsyncMock(
        return_value=[{"_id": oid, "name": "Alice"}]
    )

    result = asyncio.run(get_members(db))
    assert len(result) == 1
    assert result[0]["name"] == "Alice"
