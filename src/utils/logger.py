import logging
import json
import os


class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_object = {
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "function": os.environ.get("AWS_LAMBDA_FUNCTION_NAME", "local"),
            "request_id": os.environ.get("AWS_REQUEST_ID", "-"),
        }
        for key, value in record.__dict__.items():
            if key not in {
                "args", "asctime", "created", "exc_info", "exc_text", "filename",
                "funcName", "id", "levelname", "levelno", "lineno", "message",
                "module", "msecs", "msg", "name", "pathname", "process",
                "processName", "relativeCreated", "stack_info", "thread",
                "threadName", "taskName",
            }:
                log_object[key] = value
        if record.exc_info:
            log_object["exception"] = self.formatException(record.exc_info)
        return json.dumps(log_object, default=str)


def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler()
        handler.setFormatter(JSONFormatter())
        logger.addHandler(handler)
    log_level = os.environ.get("LOG_LEVEL", "INFO").upper()
    logger.setLevel(getattr(logging, log_level, logging.INFO))
    logger.propagate = False
    return logger
