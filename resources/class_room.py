from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import PlainClassRoomSchema, ClassRoomSchema
from models import StandardModel, SectionModel, ClassRoomModel, TeacherModel
from db import db
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

blp = Blueprint("ClassRoom", "class_room", description="Operations related to Class Room")


@blp.route("/class_room")
class ClassRoom(MethodView):
    @blp.arguments(PlainClassRoomSchema)
    @blp.response(201, ClassRoomSchema)
    def post(self, class_room_data):
        try:
            StandardModel.query.get_or_404(class_room_data["standard_id"])
            SectionModel.query.get_or_404(class_room_data["section_id"])
            if "teacher_id" in class_room_data:
                TeacherModel.query.get_or_404(class_room_data["teacher_id"])

            class_room = ClassRoomModel(**class_room_data)

            db.session.add(class_room)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(500, message=str(e))
        except Exception as e:
            abort(500, message=str(e))
        return class_room


@blp.route("/class_rooms")
class ClassRoomList(MethodView):
    @blp.response(200, ClassRoomSchema(many=True))
    def get(self):
        class_rooms = ClassRoomModel.query.all()
        return class_rooms


@blp.route("/class_room/<string:class_room_id>/class_teacher/<string:teacher_id>")
class UpdateClassTeacherToClassRoom(MethodView):
    @blp.response(200, ClassRoomSchema)
    def put(self, class_room_id, teacher_id):
        TeacherModel.query.get_or_404(teacher_id)
        try:
            class_room = ClassRoomModel.query.get_or_404(class_room_id)
            class_room.teacher_id = teacher_id

            db.session.add(class_room)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(500, message=str(e))
        except Exception as e:
            abort(500, message=str(e))
        return class_room


@blp.route("/class_room/<string:class_room_id>/class_teacher")
class RemoveClassTeacherToClassRoom(MethodView):
    @blp.response(200, ClassRoomSchema)
    def delete(self, class_room_id):
        try:
            class_room = ClassRoomModel.query.get_or_404(class_room_id)
            class_room.teacher_id = None

            db.session.add(class_room)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(500, message=str(e))
        except Exception as e:
            abort(500, message=str(e))
        return class_room
