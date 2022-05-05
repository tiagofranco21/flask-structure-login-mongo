from app_name.api.resources.books import ns as books_namespace
from app_name.api.resources.auth import ns as auth_namespace
from app_name.api.resources.users import ns as users_namespace

__all__ = [
    "books_namespace",
    "auth_namespace",
    "users_namespace"
]
