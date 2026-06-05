import json
from moto import mock_aws
from handlers.create_project import handler


def _event(body):
    return {"body": json.dumps(body)}


@mock_aws
def test_create_valid_project(dynamodb_table):
    body = {"name": "My Project", "description": "Desc", "status": "active"}
    response = handler(_event(body), None)
    assert response["statusCode"] == 201
    body = json.loads(response["body"])
    assert body["name"] == "My Project"
    assert "id" in body
    assert "created_at" in body


@mock_aws
def test_create_with_name_only(dynamodb_table):
    response = handler(_event({"name": "Minimal"}), None)
    assert response["statusCode"] == 201
    body = json.loads(response["body"])
    assert body["status"] == "active"


@mock_aws
def test_create_missing_name_returns_400(dynamodb_table):
    response = handler(_event({"description": "no name"}), None)
    assert response["statusCode"] == 400


@mock_aws
def test_create_invalid_status_returns_400(dynamodb_table):
    response = handler(_event({"name": "X", "status": "unknown"}), None)
    assert response["statusCode"] == 400


@mock_aws
def test_create_no_body_returns_400(dynamodb_table):
    response = handler({}, None)
    assert response["statusCode"] == 400


@mock_aws
def test_create_invalid_json_returns_400(dynamodb_table):
    response = handler({"body": "not-json"}, None)
    assert response["statusCode"] == 400


@mock_aws
def test_create_name_too_long_returns_400(dynamodb_table):
    response = handler(_event({"name": "x" * 101}), None)
    assert response["statusCode"] == 400
