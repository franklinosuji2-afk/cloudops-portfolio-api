import os
from utils.dynamodb import get_table
from utils.response import success, error
from utils.logger import get_logger

logger = get_logger(__name__)


def handler(event, context):
    project_id = event.get("pathParameters", {}).get("id")
    logger.info("delete_project invoked", extra={"project_id": project_id})
    if not project_id:
        return error(400, "Missing project id")
    table = get_table(os.environ["DYNAMODB_TABLE"])
    try:
        existing = table.get_item(Key={"id": project_id})
        if not existing.get("Item"):
            return error(404, f"Project '{project_id}' not found")
        table.delete_item(Key={"id": project_id})
        logger.info("delete_project success", extra={"project_id": project_id})
        return success({"message": f"Project '{project_id}' deleted"})
    except Exception:
        logger.exception("delete_project failed")
        return error(500, "Failed to delete project")
