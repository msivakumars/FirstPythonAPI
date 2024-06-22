from db import db
from sqlalchemy import Column, Integer, String


class TeacherModel(db.Model):
    __tablename__ = "teacher"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)

    class_rooms = db.relationship("ClassRoomModel", back_populates="teacher")
    teacher_standard_subjects = db.relationship("TeacherStandardSubjectModel", back_populates="teacher")
