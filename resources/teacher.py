from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import TeacherSchema, PlainTeacherSchema, UpdateTeacherSchema
from models import TeacherModel
from db import db
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

blp = Blueprint("Teacher", "teacher", description="Operations related to Teacher")


@blp.route("/teacher")
class Teacher(MethodView):
    @blp.arguments(PlainTeacherSchema)
    @blp.response(201, TeacherSchema)
    def post(self, teacher_data):
        teacher = TeacherModel(**teacher_data)
        try:
            db.session.add(teacher)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(500, message=str(e))
        return teacher


@blp.route("/teachers")
class TeacherList(MethodView):
    @blp.response(200, TeacherSchema(many=True))
    def get(self):
        teachers = TeacherModel.query.all()
        return teachers


@blp.route("/teacher/<string:teacher_id>")
class TeacherById(MethodView):
    @blp.response(200, TeacherSchema)
    def get(self, teacher_id):
        teacher = TeacherModel.query.get_or_404(teacher_id)
        return teacher

    def delete(self, teacher_id):
        teacher = TeacherModel.query.get_or_404(teacher_id)
        try:
            db.session.remove(teacher)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(500, message=str(e))
        return {"Teacher deleted"}

    @blp.arguments(UpdateTeacherSchema)
    @blp.response(200, TeacherSchema)
    def put(self, teacher_data, teacher_id):
        teacher = TeacherModel.query.get_or_404(teacher_id)
        try:
            teacher.name = teacher_data["name"]
            db.session.add(teacher)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(500, message=str(e))
        return teacher
