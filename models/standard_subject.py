from db import db
from sqlalchemy import Column, ForeignKey, Integer


class StandardSubjectModel(db.Model):
    __tablename__ = "standard_subject"

    id = Column(Integer, primary_key=True)
    standard_id = Column(Integer, ForeignKey("standard.id"), nullable=False)
    subject_id = Column(Integer, ForeignKey("subject.id"), nullable=False)

    standard = db.relationship("StandardModel", viewonly=True)
    subject = db.relationship("SubjectModel", viewonly=True)
    teacher_standard_subjects = db.relationship("TeacherStandardSubjectModel", back_populates="standard_subject")
