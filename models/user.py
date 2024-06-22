from db import db
from sqlalchemy import Column, String, Integer


class UserModel(db.Model):
    id = Column(Integer, primary_key=True)
    username = Column(String(80), unique=True, nullable=False)
    password = Column(String, nullable=False)
