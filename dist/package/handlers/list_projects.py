import os
from utils.dynamodb import get_table
from utils.response import success, error
from utils.logger import get_logger

logger = get_logger(__name__)


def handler(event, context):
    logger.info("list_projects invoked", extra={"event": event})
    table = get_table(os.environ["DYNAMODB_TABLE"])
    try:
        result = table.scan()
        items = result.get("Items", [])
        while "LastEvaluatedKey" in result:
            result = table.scan(ExclusiveStartKey=result["LastEvaluatedKey"])
            items.extend(result.get("Items", []))
        logger.info("list_projects success", extra={"count": len(items)})
        return success({"projects": items, "count": len(items)})
    except Exception:
        logger.exception("list_projects failed")
        return error(500, "Failed to retrieve projects")
