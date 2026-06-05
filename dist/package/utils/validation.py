VALID_STATUSES = {"active", "archived", "completed", "paused"}
MAX_NAME_LENGTH = 100
MAX_DESCRIPTION_LENGTH = 1000


def validate_project_input(data: dict, require_all: bool = False) -> str | None:
    if not isinstance(data, dict):
        return "Request body must be a JSON object"

    if require_all:
        if "name" not in data or not str(data["name"]).strip():
            return "'name' is required and cannot be blank"

    name = data.get("name")
    if name is not None:
        if not isinstance(name, str) or not name.strip():
            return "'name' must be a non-empty string"
        if len(name.strip()) > MAX_NAME_LENGTH:
            return f"'name' must be {MAX_NAME_LENGTH} characters or fewer"

    description = data.get("description")
    if description is not None:
        if not isinstance(description, str):
            return "'description' must be a string"
        if len(description) > MAX_DESCRIPTION_LENGTH:
            return f"'description' must be {MAX_DESCRIPTION_LENGTH} characters or fewer"

    status = data.get("status")
    if status is not None:
        if status not in VALID_STATUSES:
            return f"'status' must be one of: {sorted(VALID_STATUSES)}"

    return None
