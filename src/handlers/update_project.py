import json
import os
from datetime import datetime, timezone
from utils.dynamodb import get_table
from utils.response import success, error
from utils.validation import validate_project_input
from utils.logger import get_logger

logger = get_logger(__name__)
ALLOWED_FIELDS = {"name", "description", "status"}


def handler(event, context):
    project_id = event.get("pathParameters", {}).get("id")
    logger.info("update_project invoked", extra={"project_id": project_id})
    if not project_id:
        return error(400, "Missing project id")
    body = event.get("body")
    if not body:
        return error(400, "Request body is required")
    try:
        data = json.loads(body)
    except (json.JSONDecodeError, TypeError):
        return error(400, "Invalid JSON body")
    validation_error = validate_project_input(data, require_all=False)
    if validation_error:
        return error(400, validation_error)
    update_fields = {k: v for k, v in data.items() if k in ALLOWED_FIELDS}
    if not update_fields:
        return error(400, f"No valid fields to update. Allowed: {sorted(ALLOWED_FIELDS)}")
    table = get_table(os.environ["DYNAMODB_TABLE"])
    try:
        existing = table.get_item(Key={"id": project_id})
        if not existing.get("Item"):
            return error(404, f"Project '{project_id}' not found")
    except Exception:
        logger.exception("update_project existence check failed")
        return error(500, "Failed to verify project existence")
    update_fields["updated_at"] = datetime.now(timezone.utc).isoformat()
    expr_parts = []
    expr_names = {}
    expr_values = {}
    for key, value in update_fields.items():
        safe_key = f"#field_{key}"
        val_key = f":val_{key}"
        expr_parts.append(f"{safe_key} = {val_key}")
        expr_names[safe_key] = key
        expr_values[val_key] = value if not isinstance(value, str) else value.strip()
    update_expression = "SET " + ", ".join(expr_parts)
    try:
        result = table.update_item(
            Key={"id": project_id},
            UpdateExpression=update_expression,
            ExpressionAttributeNames=expr_names,
            ExpressionAttributeValues=expr_values,
            ReturnValues="ALL_NEW",
        )
        updated = result.get("Attributes", {})
        logger.info("update_project success", extra={"project_id": project_id})
        return success(updated)
    except Exception:
        logger.exception("update_project failed")
        return error(500, "Failed to update project")
