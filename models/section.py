from db import db
from sqlalchemy import Column, ForeignKey, Integer, String


class SectionModel(db.Model):
    __tablename__ = "section"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)

    standards = db.relationship("StandardModel", back_populates="sections", secondary="class_room")