#!/usr/bin/python
# -*- coding: utf-8 -*-
import os

import sqlalchemy
from flask import render_template, Blueprint
from sqlalchemy.orm import scoped_session, sessionmaker

from models.models_Orders import Orders

app3 = Blueprint('payment', __name__, template_folder='templates')

@app3.route('/pay', methods=['POST'])
def pay():
    price = 0
    databese_file = os.path.join(os.path.abspath(os.path.dirname(__file__)), '../models/Orders.db')
    engine = sqlalchemy.create_engine('sqlite:///' + databese_file, convert_unicode=True)
    session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
    all_beverages = session.query(Orders).all()
    for beverages in all_beverages:
        order = int(beverages.price)
        price = price + order

    return render_template("checkout.html", price=price, all_beverages=all_beverages)