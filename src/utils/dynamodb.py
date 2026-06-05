import boto3
import os

_dynamodb = None


def _get_resource():
    global _dynamodb
    if _dynamodb is None:
        kwargs = {}
        endpoint = os.environ.get("DYNAMODB_ENDPOINT_URL")
        if endpoint:
            kwargs["endpoint_url"] = endpoint
        _dynamodb = boto3.resource("dynamodb", **kwargs)
    return _dynamodb


def get_table(table_name: str):
    return _get_resource().Table(table_name)
