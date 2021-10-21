from sqlalchemy import Column, Integer, String, Text, DateTime
from models.database import Base
from datetime import datetime


class Beverages(Base):
    __tablename__ = 'beverages'
    id = Column(Integer, primary_key=True)
    title = Column(String(128), unique=True)
    body = Column(Text)
    price = Column(Text)
    zaiko = Column(Text)

    def __init__(self, title=None, body=None, price=None, zaiko=None):
        self.title = title
        self.body = body
        self.price = price
        self.zaiko = zaiko

    def __repr__(self):
        return '<Title %r>' % (self.title)


