import json
from moto import mock_aws
from handlers.delete_project import handler


def _event(project_id):
    return {"pathParameters": {"id": project_id}}


@mock_aws
def test_delete_existing_project(dynamodb_table, sample_project):
    response = handler(_event(sample_project["id"]), None)
    assert response["statusCode"] == 200
    body = json.loads(response["body"])
    assert "deleted" in body["message"].lower()


@mock_aws
def test_delete_removes_item_from_table(dynamodb_table, sample_project):
    handler(_event(sample_project["id"]), None)
    result = dynamodb_table.get_item(Key={"id": sample_project["id"]})
    assert "Item" not in result


@mock_aws
def test_delete_nonexistent_project_returns_404(dynamodb_table):
    response = handler(_event("not-there"), None)
    assert response["statusCode"] == 404


@mock_aws
def test_delete_missing_id_returns_400(dynamodb_table):
    response = handler({}, None)
    assert response["statusCode"] == 400
