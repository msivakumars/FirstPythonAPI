from db import db
from sqlalchemy import Column, ForeignKey, Integer


class TeacherStandardSubjectModel(db.Model):
    """
    This Model captures all the subjects that a teacher will take with respect to a standard
    """
    __tablename__ = "teacher_standard_subject"

    id = Column(Integer, primary_key=True)
    teacher_id = Column(Integer, ForeignKey("teacher.id"), nullable=False)
    standard_subject_id = Column(Integer, ForeignKey("standard_subject.id"), nullable=False)

    teacher = db.relationship("TeacherModel", back_populates="teacher_standard_subjects")
    standard_subject = db.relationship("StandardSubjectModel", back_populates="teacher_standard_subjects")

