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
        #limit = pay.limit
        limit = np.random.choice(["0", "1"], p=[0.3, 0.7])
        #limit = limit - price
        # if limit <= 0:
        #     limit = 0
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
    url = 'http://192.168.100.131:5001/reset'
    res_failed = requests.post(url=url)
    session.commit()
    return json.dumps({"status": "Success"})




if __name__ == "__main__":
    app3.run(debug=True, host='0.0.0.0', port=5002)