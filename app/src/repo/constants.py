from .exceptions import ErrorMessages

DEFAULT_ERROR_MESSAGE_TEMPLATES: ErrorMessages = {
    "integrity": "There was a data validation error during processing",
    "foreign_key": "A foreign key is missing or invalid",
    "multiple_rows": "Multiple matching rows found",
    "duplicate_key": "A record matching the supplied data already exists.",
    "other": "There was an error during data processing",
    "check_constraint": "The data failed a check constraint during processing",
    "not_found": "The requested resource was not found",
}
"""Default error messages for repository errors."""
