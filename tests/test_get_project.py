import json
from moto import mock_aws
from handlers.get_project import handler


def _event(project_id):
    return {"pathParameters": {"id": project_id}}


@mock_aws
def test_get_existing_project(dynamodb_table, sample_project):
    response = handler(_event(sample_project["id"]), None)
    assert response["statusCode"] == 200
    body = json.loads(response["body"])
    assert body["id"] == sample_project["id"]


@mock_aws
def test_get_missing_project_returns_404(dynamodb_table):
    response = handler(_event("does-not-exist"), None)
    assert response["statusCode"] == 404


@mock_aws
def test_get_missing_id_returns_400(dynamodb_table):
    response = handler({}, None)
    assert response["statusCode"] == 400
