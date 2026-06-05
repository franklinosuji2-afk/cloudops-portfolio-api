import os
from utils.dynamodb import get_table
from utils.response import success, error
from utils.logger import get_logger

logger = get_logger(__name__)


def handler(event, context):
    project_id = event.get("pathParameters", {}).get("id")
    logger.info("get_project invoked", extra={"project_id": project_id})
    if not project_id:
        return error(400, "Missing project id")
    table = get_table(os.environ["DYNAMODB_TABLE"])
    try:
        result = table.get_item(Key={"id": project_id})
        item = result.get("Item")
        if not item:
            return error(404, f"Project '{project_id}' not found")
        logger.info("get_project success", extra={"project_id": project_id})
        return success(item)
    except Exception:
        logger.exception("get_project failed")
        return error(500, "Failed to retrieve project")
