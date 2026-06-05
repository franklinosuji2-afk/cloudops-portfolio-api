import os
import sys
import boto3
from moto import mock_aws

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import pytest

TABLE_NAME = "test-projects"


@pytest.fixture(autouse=True)
def aws_credentials():
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"
    os.environ["AWS_DEFAULT_REGION"] = "eu-central-1"


@pytest.fixture
def dynamodb_table():
    os.environ["DYNAMODB_TABLE"] = TABLE_NAME
    with mock_aws():
        ddb = boto3.resource("dynamodb", region_name="eu-central-1")
        table = ddb.create_table(
            TableName=TABLE_NAME,
            KeySchema=[{"AttributeName": "id", "KeyType": "HASH"}],
            AttributeDefinitions=[{"AttributeName": "id", "AttributeType": "S"}],
            BillingMode="PAY_PER_REQUEST",
        )
        table.meta.client.get_waiter("table_exists").wait(TableName=TABLE_NAME)
        import utils.dynamodb as ddb_module
        ddb_module._dynamodb = None
        yield table
        ddb_module._dynamodb = None


@pytest.fixture
def sample_project(dynamodb_table):
    from datetime import datetime, timezone
    import uuid
    project = {
        "id": str(uuid.uuid4()),
        "name": "Test Project",
        "description": "A project used in tests",
        "status": "active",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "updated_at": datetime.now(timezone.utc).isoformat(),
    }
    dynamodb_table.put_item(Item=project)
    return project
