from src.repo.exceptions import ErrorMessages

PRODUCT_ERROR_MESSAGES: ErrorMessages = {
    "not_found": "Product not found",
    "duplicate_key": "A product with this name already exists",
    "integrity": "Product data is invalid",
    "foreign_key": "Product references an invalid related resource",
    "check_constraint": "Product data violates business rules",
    "multiple_rows": "Multiple products were found when only one was expected",
    "other": "An unexpected error occurred while processing the product",
}
