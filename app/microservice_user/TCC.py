#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
import os
from datetime import datetime

import sqlalchemy
from flask import render_template, request, session, redirect, url_for, Blueprint, Flask, jsonify
from sqlalchemy.orm import scoped_session, sessionmaker

from library.models.models.models_Orders import PastOrders, Orders
from library.models.models.models_User import User
from library.models.models.models_Beverages import Beverages
from hashlib import sha256
from app.microservice_main.src import key
import requests

app2 = Flask(__name__)

databese_file = os.path.join(os.path.abspath(os.path.dirname(__file__)), '../../library/models/models/User.db')
engine = sqlalchemy.create_engine('sqlite:///' + databese_file)
session2 = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

databese_file = os.path.join(os.path.abspath(os.path.dirname(__file__)), '../../library/models/models/Orders.db')
engine = sqlalchemy.create_engine('sqlite:///' + databese_file, convert_unicode=True)
session3 = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
all_order = session3.query(Orders).all()


@app2.route("/login", methods=["post"])
def login():
    data = json.loads(request.json)
    user_name = data["name"]
    user = session2.query(User).filter_by(user_name=user_name).first()
    if user:
        #hashed_password = data["password"]
        hashed_password = sha256((user_name + data["password"] + key.SALT).encode("utf-8")).hexdigest()
        if user.hashed_password == hashed_password:
            #session["user_name"] = user_name
            return json.dumps({"status": "login"})
            #return redirect(url_for("index"))
        else:
            return json.dumps({"messege" "worng_password"})
            #return redirect(url_for("top", status="wrong_password"))
    else:
        return json.dumps({"messege": "user_notfound"})
        #return redirect(url_for("top", status="user_notfound"))


@app2.route("/registar", methods=["post"])
def registar():
    data = json.loads(request.json)
    user_name = data["name"]
    #user_name = request.form["user_name"]
    user = session2.query(User).filter_by(user_name=user_name).first()
    if user:
        return json.dumps({"message": "suceeded!", "dbstatus": "healthy"})
        #return redirect(url_for("user.newcomer", status="exist_user"))
    else:
        id=0
        password = data["password"]
        id = id+1
        hashed_password = sha256((user_name + password + key.SALT).encode("utf-8")).hexdigest()
        user = User(user_name, hashed_password)
        session2.add(user)
        session2.commit()
        #session["user_name"] = user_name
        return json.dumps({"message": "suceeded!", "dbstatus": "healthy"})




@app2.route("/failed", methods=["post"])
def failed():
    all_user = session2.query(User).all()
    for user in all_user:
        print("%s入りました。", user)
        used_point = user.used_point
        user_point = user.point
        point:int = user_point + used_point
        user.point = point
        #user.used_point = 0
        session2.commit()
    #url = 'http://192.168.3.7:5000/failed'
    databese_file = os.path.join(os.path.abspath(os.path.dirname(__file__)), '../../library/models/models/Orders.db')
    engine = sqlalchemy.create_engine('sqlite:///' + databese_file, convert_unicode=True)
    session3 = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
    all_order = session3.query(Orders).all()
    for beverages in all_order:
        name = beverages.title
        failed_zaiko(name)
    return json.dumps({"status": "roll backed"})


def failed_zaiko(name):
    databese_file = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                                 '../../library/models/models/Beverages.db')
    engine = sqlalchemy.create_engine('sqlite:///' + databese_file, convert_unicode=True)
    session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
    all_beverages = session.query(Beverages).all()
    for beverages in all_beverages:
        zaiko = int(beverages.zaiko)
        if name == beverages.title:
            if zaiko != 0:
                zaiko = zaiko + 1
                beverages.zaiko = zaiko
                if int(beverages.zaiko) < 0:
                    beverages.zaiko = 0
        session.commit()
    all_order = session3.query(Orders).all()
    for i in all_order:
        print("入りました")
        datetime_before = i.date
        date_failed = datetime.now() - datetime_before
        oo = PastOrders(date_failed=date_failed.total_seconds())
        session3.add(oo)
        session3.commit()
    return 0

        #session3.add(oo)
        #all_past_order = session2.query(PastOrders).last()
        #for j in all_past_order:
            #j.datetime_after = date_failed.total_seconds()
        #session3.commit()
    # return json.dumps({"status": "roll backed"})

if __name__ == "__main__":
    app2.run(debug=True, host='0.0.0.0', port=5001)
