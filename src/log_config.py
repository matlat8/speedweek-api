from loguru import logger
import json
import sys

def json_serializer(record):
    log_entry = {
        "time": record["time"].strftime('%Y-%m-%dT%H:%M:%S.%f%z'),
        "level": record["level"].name,
        "message": record["message"],
        "file": record["file"].path,
        "function": record["function"],
        "line": record["line"],
    }
    return json.dumps(log_entry)

def setup_logging(log_file="log.json"):
    logger.remove()  # Remove the default logger
    logger.add(log_file, serialize=True)
    #logger.add('auth.log', serialize=True, filter=lambda record: record["extra"].get("module") == "auth")
    logger.add(sys.stdout, format="{time} {level} {message}", level="INFO")

# Call the setup function to configure the logger at import time
setup_logging()