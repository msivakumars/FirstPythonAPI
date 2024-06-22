from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import StandardSubjectSchema, PlainStandardSubjectSchema
from models import StandardModel, SubjectModel, StandardSubjectModel
from db import db
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

blp = Blueprint("StandardAndSubject", "standard_subject", description="Operations related to Standard and Subject")


@blp.route("/standard_subject")
class StandardAndSubject(MethodView):
    @blp.arguments(PlainStandardSubjectSchema)
    @blp.response(201, StandardSubjectSchema)
    def post(self, standard_subject_data):
        try:
            StandardModel.query.get_or_404(standard_subject_data["standard_id"])
            SubjectModel.query.get_or_404(standard_subject_data["subject_id"])

            standard_subject = StandardSubjectModel(**standard_subject_data)

            db.session.add(standard_subject)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(500, message=str(e))
        except Exception as e:
            abort(500, message=str(e))
        return standard_subject


@blp.route("/standard_subjects")
class StandardAndSubjectList(MethodView):
    @blp.response(200, StandardSubjectSchema(many=True))
    def get(self):
        standard_subjects = StandardSubjectModel.query.all()
        return standard_subjects
