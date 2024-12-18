from flask_restx import fields
from app_name.api.restplus import api

user_schema_PUT = api.model('User Schema PUT', {
    'password': fields.String(required=False, description="User password"),
    'role': fields.String(required=True,
                            enum=["master", "admin"],
                            description="User role"),
    'name': fields.String(required=True, description="User name"),
})

user_schema_POST = api.model('User Schema POST', {
    'email': fields.String(required=True, description="User email"),
    'password': fields.String(required=True, description="User password"),
    'role': fields.String(required=True,
                            enum=["master", "admin"],
                            description="User role"),
    'name': fields.String(required=True, description="User name"),
})

user_schema_dump = api.model('User Schema Dump', {
    "id": fields.String(description="User id"),
    'email': fields.String(required=True, description="User email"),
    'role': fields.String(required=True,
                            enum=["master", "admin"],
                            description="User role"),
    'name': fields.String(required=True, description="User name"),
})
