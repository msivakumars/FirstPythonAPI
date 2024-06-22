from db import db
from sqlalchemy import Column, ForeignKey, Integer, String


class StandardModel(db.Model):
    __tablename__ = "standard"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)

    sections = db.relationship("SectionModel", back_populates="standards", secondary="class_room")
    subjects = db.relationship("SubjectModel", back_populates="standards", secondary="standard_subject")