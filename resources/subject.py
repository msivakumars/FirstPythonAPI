from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import UpdateSubjectSchema, SubjectSchema, PlainSubjectSchema
from models import SubjectModel
from db import db
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

blp = Blueprint("Subject", "subject", description="Operations related to Subject")


@blp.route("/subject")
class Subject(MethodView):
    @blp.arguments(PlainSubjectSchema)
    @blp.response(201, SubjectSchema)
    def post(self, subject_data):
        subject = SubjectModel(**subject_data)
        try:
            db.session.add(subject)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(500, message=str(e))
        return subject


@blp.route("/subjects")
class SubjectList(MethodView):
    @blp.response(200,SubjectSchema(many=True))
    def get(self):
        subjects = SubjectModel.query.all()
        return subjects


@blp.route("/subject/<string:subject_id>")
class SubjectById(MethodView):
    @blp.response(200, SubjectSchema)
    def get(self, subject_id):
        subject = SubjectModel.query.get_or_404(subject_id)
        return subject

    def delete(self, subject_id):
        subject = SubjectModel.query.get_or_404(subject_id)
        try:
            db.session.remove(subject)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(500, message=str(e))
        return {"Subject deleted"}

    @blp.arguments(UpdateSubjectSchema)
    @blp.response(200, SubjectSchema)
    def put(self, subject_data, subject_id):
        subject = SubjectModel.query.get_or_404(subject_id)
        try:
            subject.name = subject_data["name"]
            db.session.add(subject)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(500, message=str(e))
        return subject
