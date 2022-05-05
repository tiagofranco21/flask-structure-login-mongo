from mongoengine import (
    signals,
    StringField,
    DateTimeField,
    BooleanField
)
from app_name.extensions import db
from app_name.models.base import BaseModel


class BlacklistToken(db.Document, BaseModel):
    """
    Blacklist Token Model for storing JWT tokens
    """
    meta = {"collection": "blacklist_tokens"}

    jti = StringField()
    token_type = StringField()
    user_identity = StringField()
    revoked = BooleanField()
    expires = DateTimeField()
    last_use = DateTimeField()

signals.pre_save.connect(BlacklistToken.pre_save, sender=BlacklistToken)
