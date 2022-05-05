from flask import request, current_app as app
from flask_restx import Resource, marshal
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity,
    get_jwt
)
from app_name.api.restplus import api
from app_name.api.schemas.login import (
    login_schema_success,
    login_schema,
    access_token_schema
)
from app_name.models import User
from app_name.helpers.authentication import (
    add_token_to_database,
    update_refresh_token,
    revoke_token
)

ns = api.namespace(
    'auth', description='Operations related to authentication')


@ns.route('/login')
class LoginResource(Resource):

    @classmethod
    @ns.response(200, "User successfully login.", login_schema_success)
    @ns.expect(login_schema, validate=True)
    def post(cls):
        """
        User Login Resource
        """
        data = request.json
        user_obj = User.objects(email=data.get('email')).first()

        if user_obj and user_obj.check_password(data.get('password')) :
            access_token = create_access_token(identity=user_obj)
            refresh_token = create_refresh_token(identity=user_obj)

            add_token_to_database(access_token, app.config['JWT_IDENTITY_CLAIM'])
            add_token_to_database(refresh_token, app.config['JWT_IDENTITY_CLAIM'])

            rest = {
                'access_token': access_token,
                'refresh_token': refresh_token
            }

            return marshal(rest, login_schema_success)

        return "Email or password is invalid", 404


@ns.route('/logout')
@api.doc(security='Authorization')
class UserLogoutAccess(Resource):

    @classmethod
    @jwt_required()
    @ns.response(200, "Access token has been revoked")
    def post(cls):

        jti = get_jwt()['jti']

        revoke_token(jti)
        return {"message": 'Access token has been revoked'}


@ns.route('/logout/refresh')
@api.doc(security='Authorization')
class UserLogoutRefresh(Resource):

    @classmethod
    @jwt_required(refresh=True)
    @ns.response(200, "Refresh token has been revoked")
    def post(cls):

        jti = get_jwt()['jti']

        revoke_token(jti)
        return {"message": 'Refresh token has been revoked'}


@ns.route('/refresh')
@api.doc(security='Authorization')
class TokenRefresh(Resource):

    @classmethod
    @jwt_required(refresh=True)
    @ns.response(200, "Access token successfully generated", access_token_schema)
    def post(cls):
        jti = get_jwt()['jti']

        if update_refresh_token(jti):
            current_user = User.objects.get_or_404(email=get_jwt_identity())

            access_token = create_access_token(identity=current_user)
            add_token_to_database(access_token, app.config['JWT_IDENTITY_CLAIM'])

            return {'access_token': access_token}

        return {'message': 'Something went wrong'}, 500
