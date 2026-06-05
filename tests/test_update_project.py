import json
from moto import mock_aws
from handlers.update_project import handler


def _event(project_id, body):
    return {"pathParameters": {"id": project_id}, "body": json.dumps(body)}


@mock_aws
def test_update_name(dynamodb_table, sample_project):
    response = handler(_event(sample_project["id"], {"name": "Updated Name"}), None)
    assert response["statusCode"] == 200
    body = json.loads(response["body"])
    assert body["name"] == "Updated Name"


@mock_aws
def test_update_status(dynamodb_table, sample_project):
    response = handler(_event(sample_project["id"], {"status": "archived"}), None)
    assert response["statusCode"] == 200
    body = json.loads(response["body"])
    assert body["status"] == "archived"


@mock_aws
def test_update_multiple_fields(dynamodb_table, sample_project):
    response = handler(_event(sample_project["id"], {
        "name": "New Name", "description": "New desc", "status": "completed",
    }), None)
    assert response["statusCode"] == 200
    body = json.loads(response["body"])
    assert body["name"] == "New Name"
    assert body["status"] == "completed"


@mock_aws
def test_update_nonexistent_project_returns_404(dynamodb_table):
    response = handler(_event("ghost-id", {"name": "X"}), None)
    assert response["statusCode"] == 404


@mock_aws
def test_update_invalid_status_returns_400(dynamodb_table, sample_project):
    response = handler(_event(sample_project["id"], {"status": "broken"}), None)
    assert response["statusCode"] == 400


@mock_aws
def test_update_no_valid_fields_returns_400(dynamodb_table, sample_project):
    response = handler(_event(sample_project["id"], {"unknown_field": "value"}), None)
    assert response["statusCode"] == 400


@mock_aws
def test_update_timestamps_are_updated(dynamodb_table, sample_project):
    import time
    original = sample_project["updated_at"]
    time.sleep(0.01)
    response = handler(_event(sample_project["id"], {"name": "Changed"}), None)
    body = json.loads(response["body"])
    assert body["updated_at"] != original
