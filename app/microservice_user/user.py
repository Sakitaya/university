#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
import os
import sqlalchemy
from flask import render_template, request, session, redirect, url_for, Blueprint, Flask, jsonify
from sqlalchemy.orm import scoped_session, sessionmaker
from library.models.models.models_User import User
from hashlib import sha256
from app.microservice_main.src import key
import requests

app2 = Flask(__name__)

databese_file = os.path.join(os.path.abspath(os.path.dirname(__file__)), '../../library/models/models/User.db')
engine = sqlalchemy.create_engine('sqlite:///' + databese_file)
session2 = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))


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





if __name__ == "__main__":
    app2.run(debug=True, host='0.0.0.0', port=5001)
