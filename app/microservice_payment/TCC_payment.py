#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
import os
import random
from datetime import datetime

import numpy as np
import sqlalchemy
from flask import render_template, request, redirect, url_for, Blueprint, Flask, jsonify
from sqlalchemy.orm import scoped_session, sessionmaker

from library.models.models.models_Beverages import Beverages
from library.models.models.models_Orders import PastOrders, Orders
from library.models.models.models_User import User
from library.models.models.models_payment import Payment, Used
from hashlib import sha256
from app.microservice_main.src import key
import requests

app3 = Flask(__name__)
databese_file = os.path.join(os.path.abspath(os.path.dirname(__file__)), '../../library/models/models/Payment.db')
engine = sqlalchemy.create_engine('sqlite:///' + databese_file)
session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))


@app3.route("/payment", methods=["post"])
def payment():
    print("入りました")
    all_pay = session.query(Payment).all()
    for pay in all_pay:
        data = json.loads(request.json)
        price = data["price"]
        limit = int(data["limit"])
        # limit = pay.limit
        # limit = np.random.choice(["0", "1"], p=[0.1, 0.9])
        #limit = limit - price
        # if limit == 0:
        #     limit = 10000
        pay.limit = limit
        oo = Used(used=price)
        session.add(oo)
    session.commit()
    if limit == 0:
        return json.dumps({"status": "failed"})
    else:
        return json.dumps({"status": "Success"})


@app3.route("/reset", methods=["post"])
def reset():
    all_pay = session.query(Payment).all()
    for pay in all_pay:
        pay.limit = 5000
    url = 'http://192.168.100.63:5001/reset'
    res_failed = requests.post(url=url)
    session.commit()
    return json.dumps({"status": "Success"})





@app3.route("/success", methods=["post"])
def success():
    url = 'http://192.168.100.63:5004/saga_success'
    requests.post(url=url)
    name = None
    databese_file = os.path.join(os.path.abspath(os.path.dirname(__file__)), '../../library/models/models/Orders.db')
    engine = sqlalchemy.create_engine('sqlite:///' + databese_file, convert_unicode=True)
    session3 = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
    content = session3.query(Orders).all()
    databese_file = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                                 '../../library/models/models/Beverages.db')
    engine = sqlalchemy.create_engine('sqlite:///' + databese_file, convert_unicode=True)
    session2 = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
    content_Bverages = session2.query(Beverages).all()
    content_Orders = session3.query(Orders).all()
    for i in content_Orders:
        name = i.title
    for beverages in content_Bverages:
        if name == beverages.title:
            with open("../microservice_stock/.zaiko.csv", "r", encoding='utf-8') as file:
                # zaiko = int(beverages.zaiko)
                zaiko = int(file.read())
                zaiko = zaiko - 1
                beverages.zaiko = zaiko
                if int(beverages.zaiko) < 0:
                    beverages.zaiko = 0
                session2.commit()
    databese_file = os.path.join(os.path.abspath(os.path.dirname(__file__)), '../../library/models/models/User.db')
    engine = sqlalchemy.create_engine('sqlite:///' + databese_file, convert_unicode=True)
    session4 = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
    all_user = session4.query(User).all()
    with open("../microservice_stock/.user_point.csv", "r", encoding='utf-8') as file:
        u_point_int = int(file.read())
    for user in all_user:
            user.point = u_point_int
            # user.used_point = point
            session4.commit()
    for i in content_Orders:
        datetime_before = i.date
        date = datetime.now() - datetime_before
        title = i.title
        status = "2"
        oo = PastOrders(title=title, status=status, date_after=date.total_seconds())
        session3.add(oo)
        session3.commit()
    return json.dumps({"status": "103"})



if __name__ == "__main__":
    app3.run(debug=True, host='0.0.0.0', port=5006)