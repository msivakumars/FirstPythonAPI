import os
from flask import Flask, jsonify
from flask_smorest import Api
from resources.user import blp as user_blue_print
from resources.standard import blp as standard_blue_print
from resources.section import blp as section_blue_print
from resources.class_room import blp as class_room_blue_print
from resources.teacher import blp as teacher_blue_print
from resources.subject import blp as subject_blue_print
from resources.standard_subject import blp as standard_and_subject_blue_print
from resources.teacher_standard_subject import blp as teacher_standard_subject_blue_print
from flask_migrate import Migrate
from db import db
from flask_jwt_extended import JWTManager, jwt_required, get_jwt
import secrets
from blocklist import BLOCKLIST

tok = secrets.SystemRandom().getrandbits(128)


def create_app(db_url=None):
    app = Flask(__name__)
    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "First Python API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv("DATABASE_URL", "sqlite:///data.db")
    app.config["SQLALCHEMY_TRACK_NOTIFICATIONS"] = False
    app.config["JWT_SECRET_KEY"] = "137951886426508653722587015693140887494"
    db.init_app(app)
    migrate = Migrate(app, db)
    jwt = JWTManager(app)

    @jwt.token_in_blocklist_loader
    def check_if_token_in_blocklist(jwt_header, jwt_payload):
        return jwt_payload["jti"] in BLOCKLIST

    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        return (
            jsonify(
                {"description": "The token has been revoked.", "error": "token_revoked"}
            ),
            401,
        )

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return jsonify(
            {
                "message": "Token has been expired",
                "error": "Token expired"
            }
        )

    @jwt.invalid_token_loader
    def expired_token_callback(jwt_payload):
        return jsonify(
            {
                "message": "Signature is not verified",
                "error": "Invalid Token"
            }
        )

    @jwt.unauthorized_loader
    def unauthorized_token_callback(jwt_payload):
        return jsonify(
            {
                "message": "Missing authorization",
                "error": "Authorization required"
            }
        )

    api = Api(app)
    api.register_blueprint(blp=user_blue_print)
    api.register_blueprint(blp=standard_blue_print)
    api.register_blueprint(blp=section_blue_print)
    api.register_blueprint(blp=class_room_blue_print)
    api.register_blueprint(blp=teacher_blue_print)
    api.register_blueprint(blp=subject_blue_print)
    api.register_blueprint(blp=standard_and_subject_blue_print)
    api.register_blueprint(blp=teacher_standard_subject_blue_print)

    return app
