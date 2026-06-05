import json
import os
import uuid
from datetime import datetime, timezone
from utils.dynamodb import get_table
from utils.response import success, error
from utils.validation import validate_project_input
from utils.logger import get_logger

logger = get_logger(__name__)


def handler(event, context):
    logger.info("create_project invoked")
    body = event.get("body")
    if not body:
        return error(400, "Request body is required")
    try:
        data = json.loads(body)
    except (json.JSONDecodeError, TypeError):
        return error(400, "Invalid JSON body")
    validation_error = validate_project_input(data, require_all=True)
    if validation_error:
        return error(400, validation_error)
    now = datetime.now(timezone.utc).isoformat()
    project = {
        "id": str(uuid.uuid4()),
        "name": data["name"].strip(),
        "description": data.get("description", "").strip(),
        "status": data.get("status", "active"),
        "created_at": now,
        "updated_at": now,
    }
    table = get_table(os.environ["DYNAMODB_TABLE"])
    try:
        table.put_item(Item=project)
        logger.info("create_project success", extra={"project_id": project["id"]})
        return success(project, status_code=201)
    except Exception:
        logger.exception("create_project failed")
        return error(500, "Failed to create project")
