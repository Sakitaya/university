import os

import sqlalchemy
from sqlalchemy.orm import scoped_session, sessionmaker


def beverage():
    databese_file = os.path.join(os.path.abspath(os.path.dirname(__file__)), '../library/models/models/Beverages.db')
    engine = sqlalchemy.create_engine('sqlite:///' + databese_file, convert_unicode=True)
    session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
    return session


def order():
    databese_file = os.path.join(os.path.abspath(os.path.dirname(__file__)), '../library/models/models/Orders.db')
    engine = sqlalchemy.create_engine('sqlite:///' + databese_file, convert_unicode=True)
    session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
    return session


def user():
    databese_file = os.path.join(os.path.abspath(os.path.dirname(__file__)), '../library/models/models/User.db')
    engine = sqlalchemy.create_engine('sqlite:///' + databese_file, convert_unicode=True)
    session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
    return session