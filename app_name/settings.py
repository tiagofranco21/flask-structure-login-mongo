from decouple import config

ENV = config("ENV")
DEBUG = ENV == "development"
SECRET_KEY = config("SECRET_KEY")
PORT = config("PORT")

# Flask settings
FLASK_DEBUG = DEBUG  # Do not use debug mode in production


# MongoDB settings
MONGODB_SETTINGS = {
    "db": config("MONGO_DB"),
    "host": config("MONGO_HOST") if config("MONGO_HOST") else "localhost",
    "port": int(config("MONGO_PORT")) if config("MONGO_PORT") else 27017,
    "username": config("MONGO_USER") if config("MONGO_USER") else "",
    "password": config("MONGO_PASS") if config("MONGO_PASS") else "",
    "authentication_source": "admin",
}


# Flask-Restplus settings
SWAGGER_UI_DOC_EXPANSION = 'list'
RESTPLUS_VALIDATE = True
RESTPLUS_MASK_SWAGGER = False
ERROR_404_HELP = False

# Secret key for signing cookies
JWT_SECRET_KEY = SECRET_KEY

JWT_BLACKLIST_ENABLED = True
JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']

JWT_ACCESS_TOKEN_EXPIRES = 86400 # one day
JWT_REFRESH_TOKEN_EXPIRES = 15552000 # six months
