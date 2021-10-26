from sqlalchemy import Column, Integer, String, Text
from library.models.models.database import Base


class Orders(Base):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True)
    title = Column(String(128), unique=False)
    body = Column(Text)
    price = Column(Text)


    def __init__(self, title=None, body=None, price=None):
        self.title = title
        self.body = body
        self.price = price

    def __repr__(self):
        return '<Title %r>' % (self.title)