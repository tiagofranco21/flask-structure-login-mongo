from flask import request
from flask_restx import Resource, marshal, fields
from mongoengine import ValidationError
from app_name.api.schemas.user import (
    user_schema_PUT,
    user_schema_POST,
    user_schema_dump,
)
from app_name.models import User
from app_name.api.restplus import api
from app_name.api.middleware import access_required

ns = api.namespace(
    'users', description='Operations related to users')

# Default response for POST and PUT
schema_response = api.model('User Response', {
    'user_id': fields.String(),
})


@ns.route('/')
class UserCollection(Resource):

    @classmethod
    @api.doc(security='Authorization')
    @ns.marshal_list_with(user_schema_dump)
    @access_required(["master"])
    def get(cls):
        """
        Returns all users.
        """

        users = User.objects()

        users_dump = []
        for user in users:
            users_dump.append(marshal(user, user_schema_dump))

        return users_dump

    @classmethod
    @ns.response(201, "User successfully created.", schema_response)
    @ns.response(400, "Email already registered.")
    @ns.expect(user_schema_POST, validate=True)
    def post(cls):
        """
        Creates a new user.
        """
        data = request.json
        user_obj = User.objects(email=data.get("email")).first()
        if user_obj:
            return {'message': "Email already registered"}, 400

        user_new = User(
            email=data.get("email"),
            password=User.generate_hash(data.get("password")),
            role=data.get("role"),
            name=data.get("name"),
        )

        try:
            user_new.save()
        except ValidationError:
            return {"message": "Unexpected error"}, 500

        result = {
            "user_id": str(user_new.id)
        }

        return result, 201


@ns.route('/<string:user_id>')
@ns.response(404, 'User not found.')
@api.doc(security='Authorization')
class UserItem(Resource):

    @classmethod
    @ns.marshal_with(user_schema_dump)
    @access_required(["master"])
    def get(cls, user_id):
        """
        Returns a user.
        """

        user_obj = User.objects.get_or_404(id=user_id)

        return marshal(user_obj, user_schema_dump)

    @classmethod
    @ns.expect(user_schema_PUT, validate=True)
    @ns.response(200, 'User successfully updated.', schema_response)
    @access_required(["master"])
    def put(cls, user_id):
        """
        Updates a User.
        """
        user_obj = User.objects.get_or_404(id=user_id)
        data = request.json

        user_obj.name = data.get('name')
        user_obj.role = data.get('role')

        if data.get('password'):
            user_obj.password = User.generate_hash(data.get('password'))

        try:
            user_obj.save()
        except ValidationError:
            return {"message": "Unexpected error"}, 500

        result = {
            "user_id": str(user_obj.id)
        }

        return result

    @classmethod
    @ns.response(204, 'User successfully deleted.')
    @access_required(["master"])
    def delete(cls, user_id):
        """
        Deletes User.
        """
        user_obj = User.objects.get_or_404(id=user_id)

        try:
            user_obj.delete()
        except ValidationError:
            return {"message": "Unexpected error"}, 500

        return None, 204
