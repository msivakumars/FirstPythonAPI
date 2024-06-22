from db import db
from sqlalchemy import Column, Integer, String


class SubjectModel(db.Model):
    __tablename__ = "subject"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)

    standards = db.relationship("StandardModel", back_populates="subjects", secondary="standard_subject")