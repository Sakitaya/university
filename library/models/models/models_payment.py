from sqlalchemy import Column, Integer, String, Text
from models.database import Base


class Payment(Base):
    __tablename__ = 'payment'
    id = Column(Integer, primary_key=True)
    limit = Column(Integer)

    def __init__(self, limit=None):
        self.limit = limit


    def __repr__(self):
        return '<limit %r>' % self.limit


class Used(Base):
    __tablename__ = 'used'
    id = Column(Integer, primary_key=True)
    used = Column(Integer)

    def __init__(self, used=None):
        self.used = used


    def __repr__(self):
        return '<used %r>' % self.used