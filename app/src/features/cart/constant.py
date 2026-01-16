from src.repo.exceptions import ErrorMessages

CART_ERROR_MESSAGES: ErrorMessages = {
    "not_found": "Cart not found",
    "duplicate_key": "A cart already exists for this user",
    "integrity": "Cart data is invalid",
    "foreign_key": "Cart references an invalid user or related resource",
    "check_constraint": "Cart data violates business rules",
    "multiple_rows": "Multiple carts were found when only one was expected",
    "other": "An unexpected error occurred while processing the cart",
}


CART_ITEM_ERROR_MESSAGES: ErrorMessages = {
    "not_found": "Cart item not found",
    "duplicate_key": "This product is already in the cart",
    "integrity": "Cart item data is invalid",
    "foreign_key": "Cart item references an invalid cart or product",
    "check_constraint": "Cart item data violates business rules",
    "multiple_rows": "Multiple cart items were found when only one was expected",
    "other": "An unexpected error occurred while processing the cart item",
}
