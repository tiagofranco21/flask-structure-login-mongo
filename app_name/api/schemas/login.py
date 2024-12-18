from flask_restx import fields
from app_name.api.restplus import api


login_schema_success = api.model('Login Success', {
    'access_token': fields.String(required=True),
    'refresh_token': fields.String(required=True),
})

login_schema = api.model('Login Form', {
    'email': fields.String(required=True),
    'password': fields.String(required=True),
})

access_token_schema = api.model('Login Success', {
    'access_token': fields.String(required=True),
})

logout_schema = api.model('Logout Form', {
    'access_token': fields.String(required=True),
    'refresh_token': fields.String(required=True),
})
