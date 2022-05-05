from functools import wraps
from flask_jwt_extended import verify_jwt_in_request, get_jwt

def access_required(allowed_roles=None):
    if allowed_roles is None:
        allowed_roles = []

    def token_required(func):
        @wraps(func)
        def decorated(self, *args, **kwargs):
            verify_jwt_in_request()
            role = get_jwt()["role"]

            if len(allowed_roles) > 0 and role not in allowed_roles:
                return {'message': "User does not have access"}, 401

            return func(self, *args, **kwargs)

        return decorated
    return token_required
