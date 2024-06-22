from db import db
from sqlalchemy import Column, ForeignKey, Integer, String


class ClassRoomModel(db.Model):
    __tablename__ = "class_room"

    id = Column(Integer, primary_key=True)
    standard_id = Column(Integer, ForeignKey("standard.id"), nullable=False)
    section_id = Column(Integer, ForeignKey("section.id"), nullable=False)
    teacher_id = Column(Integer, ForeignKey("teacher.id"), nullable=True)

    standard = db.relationship("StandardModel", viewonly=True)
    section = db.relationship("SectionModel", viewonly=True)
    teacher = db.relationship("TeacherModel", back_populates="class_rooms")
