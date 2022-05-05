from mongoengine import (
    signals,
    StringField,
)
from werkzeug.security import generate_password_hash, check_password_hash
from app_name.extensions import db
from app_name.models.base import BaseModel


class User(db.Document, BaseModel):
    """ User Model for storing user related details """
    meta = {"collection": "users"}

    email = StringField(unique=True, nullable=False)
    password = StringField(nullable=False)
    role = StringField(nullable=False,  default="master") # [master, admin]
    name = StringField(nullable=False)

    @staticmethod
    def generate_hash(password):
        """Hash password before saving."""
        return generate_password_hash(password)

    def check_password(self, password):
        """Check password hash against a pwd provided by user."""
        return check_password_hash(self.password, password)

signals.pre_save.connect(User.pre_save, sender=User)
