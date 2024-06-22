from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import TeacherStandardSubjectSchema, PlainTeacherStandardSubjectSchema
from models import TeacherModel, TeacherStandardSubjectModel, StandardSubjectModel
from db import db
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

blp = Blueprint("TeacherStandardSubject", "teacher_standard_subject", description="Operations related to Class Room")


@blp.route("/teacher_standard_subject")
class TeacherStandardSubject(MethodView):
    @blp.arguments(PlainTeacherStandardSubjectSchema)
    @blp.response(201, TeacherStandardSubjectSchema)
    def post(self, teacher_standard_subject_data):
        try:
            StandardSubjectModel.query.get_or_404(teacher_standard_subject_data["standard_subject_id"])
            TeacherModel.query.get_or_404(teacher_standard_subject_data["teacher_id"])

            teacher_standard_subject = TeacherStandardSubjectModel(**teacher_standard_subject_data)

            db.session.add(teacher_standard_subject)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(500, message=str(e))
        except Exception as e:
            abort(500, message=str(e))
        return teacher_standard_subject


@blp.route("/teacher_standard_subjects")
class TeacherStandardSubjectList(MethodView):
    @blp.response(200, TeacherStandardSubjectSchema(many=True))
    def get(self):
        teacher_standard_subjects = TeacherStandardSubjectModel.query.all()
        return teacher_standard_subjects


@blp.route("/teacher_standard_subject/<string:teacher_standard_subject_id>/teacher/<string:teacher_id>")
class UpdateTeacherToTeacherStandardSubject(MethodView):
    @blp.response(200, TeacherStandardSubjectSchema)
    def put(self, teacher_standard_subject_id, teacher_id):
        TeacherModel.query.get_or_404(teacher_id)
        try:
            teacher_standard_subject = TeacherStandardSubjectModel.query.get_or_404(teacher_standard_subject_id)
            teacher_standard_subject.teacher_id = teacher_id

            db.session.add(teacher_standard_subject)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(500, message=str(e))
        except Exception as e:
            abort(500, message=str(e))
        return teacher_standard_subject


@blp.route("/teacher_standard_subject/<string:teacher_standard_subject_id>/standard_subject/<string:standard_subject_id>")
class UpdateTeacherToTeacherStandardSubject(MethodView):
    @blp.response(200, TeacherStandardSubjectSchema)
    def put(self, teacher_standard_subject_id, standard_subject_id):
        StandardSubjectModel.query.get_or_404(standard_subject_id)
        try:
            teacher_standard_subject = TeacherStandardSubjectModel.query.get_or_404(teacher_standard_subject_id)
            teacher_standard_subject.standard_subject_id = standard_subject_id

            db.session.add(teacher_standard_subject)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(500, message=str(e))
        except Exception as e:
            abort(500, message=str(e))
        return teacher_standard_subject
