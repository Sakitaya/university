from datetime import datetime

from sqlalchemy import Column, Integer, String, Text, DateTime
from models.database import Base


class Orders(Base):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True)
    title = Column(String(128), unique=False)
    body = Column(Text)
    price = Column(Text)

    def __init__(self, title=None, body=None, price=None):
        super().__init__(title=None, body=None, price=None)
        self.title = title
        self.body = body
        self.price = price

    def __repr__(self):
        return '<Title %r>' % (self.title)


class PastOrders(Base):
    __tablename__ = 'pastorders'
    id = Column(Integer, primary_key=True)
    title = Column(String(128), unique=False)
    status = Column(String(128))
    date_before = Column(DateTime, default=datetime.now())
    date_after = Column(String(128))

    def __init__(self, title=None, status=None, date_before=None, date_after=None):
        self.title = title
        self.status = status
        self.date_before = date_before
        self.date_after = date_after

    def __repr__(self):
        return '<Title %r>' % (self.title)
