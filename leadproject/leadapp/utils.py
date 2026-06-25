import logging

logger = logging.getLogger(__name__)

def log_validation_error(api_name, errors):
    logger.error(
        f"Status Code: 400 | API: {api_name} | Validation Error | {errors}"
    )

def log_not_found(api_name, message):
    logger.error(
        f"Status Code: 404 | API: {api_name} | {message}"
    )

def log_exception(api_name, exception):
    logger.exception(
        f"Status Code: 500 | API: {api_name} | {str(exception)}"
    )