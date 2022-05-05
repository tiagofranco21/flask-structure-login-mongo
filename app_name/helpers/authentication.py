from datetime import datetime
from flask_jwt_extended import decode_token
from app_name.models import BlacklistToken
from app_name.extensions import jwt

@jwt.token_in_blocklist_loader
def check_if_token_in_blacklist(token_header, token_payload):
    """
    Verify if the token is revoked
    """
    jti = token_payload['jti']
    return is_token_revoked(jti)

@jwt.additional_claims_loader
def add_claims_to_access_token(user):
    """
    Create a function that will be called whenever create_access_token
    is used. It will take whatever object is passed into the
    create_access_token method, and lets us define what custom claims
    should be added to the access token.
    """
    return {
        'name': user["name"],
        'role': user["role"],
    }

@jwt.user_identity_loader
def user_identity_lookup(user):
    """
    Create a function that will be called whenever create_access_token
    is used. It will take whatever object is passed into the
    create_access_token method, and lets us define what the identity
    of the access token should be.
    """
    return user["email"]

def _epoch_utc_to_datetime(epoch_utc):
    """
    Helper function for converting epoch timestamps (as stored in JWTs) into
    python datetime objects (which are easier to use with sqlalchemy).
    """
    return datetime.fromtimestamp(epoch_utc)

def add_token_to_database(encoded_token, identity_claim):
    """
    Adds a new token to the database. It is not revoked when it is added.
    :param identity_claim:
    """
    decoded_token = decode_token(encoded_token)
    jti = decoded_token['jti']
    token_type = decoded_token['type']
    user_identity = decoded_token[identity_claim]
    expires = _epoch_utc_to_datetime(decoded_token['exp'])
    last_use = datetime.now
    revoked = False

    token = BlacklistToken(
        jti=jti,
        token_type=token_type,
        user_identity=user_identity,
        expires=expires,
        revoked=revoked,
        last_use=last_use
    )

    token.save()

def is_token_revoked(jti):
    """
    Checks if the given token is revoked or not. Because we are adding all the
    tokens that we create into this database, if the token is not present
    in the database we are going to consider it revoked, as we don't know where
    it was created.
    """

    token = BlacklistToken.objects(jti = jti).first()

    if (token):
        return token.revoked 
    else:
        return True

def revoke_token(jti):
    """
    Revokes the given token. Raises a TokenNotFound error if the token does
    not exist in the database
    """
    revoked_token = BlacklistToken.objects(jti = jti).first()
    if(revoked_token): 
        revoked_token.revoked = True
        revoked_token.save()
        return True
    else: 
        return False

def update_refresh_token(jti):
    """
    Updates the last time the refresh token was used to generate an access token
    """
    refresh_token = BlacklistToken.objects(jti = jti).first()
    
    if(refresh_token): 
        if(abs((refresh_token.last_use - datetime.now()).days) < 180):
            refresh_token.last_use = datetime.now()
            refresh_token.save()
            return True
        else:
            return False
    else: 
        return False    