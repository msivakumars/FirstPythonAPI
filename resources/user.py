from flask.views import MethodView
from flask_smorest import Blueprint, abort
from models import UserModel
from schemas import UserSchema
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from flask_jwt_extended import (JWTManager, create_access_token, create_refresh_token, get_jwt, jwt_required,
                                get_jwt_identity)
from passlib.hash import pbkdf2_sha256
from db import db
from flask import jsonify
from blocklist import BLOCKLIST

blp = Blueprint("User", "user", description="Operation related to user")


@blp.route("/register")
class UserRegistration(MethodView):
    @blp.arguments(UserSchema)
    @blp.response(201, UserSchema)
    def post(self, user_data):
        user = UserModel(
            username=user_data["username"],
            password=pbkdf2_sha256.hash(user_data["password"])
        )
        try:
            db.session.add(user)
            db.session.commit()
            return user
        except IntegrityError:
            abort(400, message="User with that name already exist")
        except SQLAlchemyError as e:
            abort(500, message=str(e))


@blp.route("/login")
class LogIn(MethodView):
    @blp.arguments(UserSchema)
    def post(self, user_data):
        try:
            user = UserModel.query.filter(
                UserModel.username==user_data["username"]
            ).first()
            if user and pbkdf2_sha256.verify(user_data["password"], user.password):
                jwt_token = create_access_token(identity=user.id, fresh=True)
                refresh_token= create_refresh_token(identity=user.id)
                return jsonify(
                    {
                        "jwt_token": jwt_token,
                        "refresh_token": refresh_token
                    }
                ), 200
            return jsonify(
                {
                    "message": "Invalid credentials"
                }
            ), 401
        except SQLAlchemyError as e:
            abort(500, message=str(e))


@blp.route("/non-fresh-token")
class NonFreshToken(MethodView):
    @jwt_required(refresh=True)
    def post(self):
        current_user = get_jwt_identity()
        jwt_token = create_access_token(identity=current_user, fresh=False)
        return jsonify(
            {
                "jwt_token": jwt_token
            }
        ), 200


@blp.route("/logout")
class LogOut(MethodView):
    @jwt_required()
    def post(self):
        jti = get_jwt()["jti"]
        BLOCKLIST.add(jti)
        return jsonify(
            {"message": "Logged out successfully"}
        ), 200


@blp.route("/users")
class UserList(MethodView):
    @blp.response(200, UserSchema(many=True))
    def get(self):
        users = UserModel.query.all()
        return users


@blp.route("/user/<int:user_id>")
class UserById(MethodView):
    @blp.response(200, UserSchema)
    def get(self, user_id):
        try:
            user = UserModel.query.get(user_id)
            return user
        except KeyError:
            abort(404, message=f"User does not exist for id {user_id}")
        except SQLAlchemyError as e:
            abort(500, message=str(e))

    def delete(self, user_id):
        try:
            user = UserModel.query.get(user_id)
            db.session.delete(user)
            db.session.commit()
            return {"message": "User deleted"}
        except KeyError:
            abort(404, message=f"User does not exist for id {user_id}")
        except SQLAlchemyError as e:
            abort(500, message=str(e))