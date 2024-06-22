from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import StandardSchema, PlainStandardSchema, UpdateStandardSchema
from models import StandardModel, SubjectModel
from db import db
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from flask_jwt_extended import jwt_required

blp = Blueprint("Standard", "standard", description="Operations related to Standard")


@blp.route("/standard")
class Standard(MethodView):
    @jwt_required()
    @blp.arguments(PlainStandardSchema)
    @blp.response(201, StandardSchema)
    def post(self, standard_data):
        standard = StandardModel(**standard_data)
        try:
            db.session.add(standard)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(500, message=str(e))
        return standard


@blp.route("/standards")
class StandardList(MethodView):
    @jwt_required()
    @blp.response(200,StandardSchema(many=True))
    def get(self):
        standards = StandardModel.query.all()
        return standards


@blp.route("/standard/<string:standard_id>")
class StandardById(MethodView):
    @jwt_required()
    @blp.response(200, StandardSchema)
    def get(self, standard_id):
        standard = StandardModel.query.get_or_404(standard_id)
        return standard

    @jwt_required(fresh=True)
    def delete(self, standard_id):
        standard = StandardModel.query.get_or_404(standard_id)
        try:
            db.session.delete(standard)
            db.session.commit()
            return {"Standard deleted"}
        except SQLAlchemyError as e:
            abort(500, message=str(e))

    @jwt_required()
    @blp.arguments(UpdateStandardSchema)
    @blp.response(200, StandardSchema)
    def put(self, standard_data, standard_id):
        standard = StandardModel.query.get_or_404(standard_id)
        try:
            standard.name = standard_data["name"]
            db.session.add(standard)
            db.session.commit()
            return standard
        except SQLAlchemyError as e:
            abort(500, message=str(e))
