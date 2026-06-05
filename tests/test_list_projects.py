import json
from moto import mock_aws
from handlers.list_projects import handler


@mock_aws
def test_list_returns_empty_when_no_projects(dynamodb_table):
    response = handler({}, None)
    assert response["statusCode"] == 200
    body = json.loads(response["body"])
    assert body["projects"] == []
    assert body["count"] == 0


@mock_aws
def test_list_returns_existing_projects(dynamodb_table, sample_project):
    response = handler({}, None)
    assert response["statusCode"] == 200
    body = json.loads(response["body"])
    assert body["count"] == 1
    assert body["projects"][0]["id"] == sample_project["id"]


@mock_aws
def test_list_returns_multiple_projects(dynamodb_table):
    from datetime import datetime, timezone
    import uuid
    for i in range(3):
        dynamodb_table.put_item(Item={
            "id": str(uuid.uuid4()),
            "name": f"Project {i}",
            "description": "",
            "status": "active",
            "created_at": datetime.now(timezone.utc).isoformat(),
            "updated_at": datetime.now(timezone.utc).isoformat(),
        })
    response = handler({}, None)
    body = json.loads(response["body"])
    assert body["count"] == 3
