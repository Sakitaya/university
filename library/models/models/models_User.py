from sqlalchemy import Column, Integer, String, Text
from models.database import Base

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    user_name = Column(String(128), unique=True)
    hashed_password = Column(String(128))
    point = Column(Integer)
    used_point = Column(Integer)
    cancel_count = Column(Integer)

    def __init__(self, user_name=None, hashed_password=None, point=0, used_point=0, cancel_count=0):
        self.user_name = user_name
        self.hashed_password = hashed_password
        self.point = point
        self.used_point = used_point
        self.cancel_count = cancel_count

    def __repr__(self):
        return '<Name %r>' % (self.user_name)