from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import SectionSchema, PlainSectionSchema, UpdateSectionSchema
from models import SectionModel
from db import db
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

blp = Blueprint("Section", "section", description="Operations related to Section")


@blp.route("/section")
class Section(MethodView):
    @blp.arguments(PlainSectionSchema)
    @blp.response(201, SectionSchema)
    def post(self, section_data):
        section = SectionModel(**section_data)
        try:
            db.session.add(section)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(500, message=str(e))
        return section


@blp.route("/sections")
class SectionList(MethodView):
    @blp.response(200, SectionSchema(many=True))
    def get(self):
        sections = SectionModel.query.all()
        return sections


@blp.route("/section/<string:section_id>")
class SectionById(MethodView):
    @blp.response(200, SectionSchema)
    def get(self, section_id):
        section = SectionModel.query.get_or_404(section_id)
        return section

    def delete(self, section_id):
        section = SectionModel.query.get_or_404(section_id)
        try:
            db.session.remove(section)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(500, message=str(e))
        return {"Section deleted"}

    @blp.arguments(UpdateSectionSchema)
    @blp.response(200, SectionSchema)
    def put(self, section_data, section_id):
        section = SectionModel.query.get_or_404(section_id)
        try:
            section.name = section_data["name"]
            db.session.add(section)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(500, message=str(e))
        return section
