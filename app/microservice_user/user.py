#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import sqlalchemy
from flask import render_template, request, session, redirect, url_for,  Blueprint
from sqlalchemy.orm import scoped_session, sessionmaker
from models.models_User import User
from hashlib import sha256
from app.microservice_main.app import key


app2 = Blueprint('user', __name__, template_folder='../templates')

databese_file = os.path.join(os.path.abspath(os.path.dirname(__file__)), '../../models/User.db')
engine = sqlalchemy.create_engine('sqlite:///' + databese_file, convert_unicode=True)
session2 = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

@app2.route("/login", methods=["post"])
def login():
    user_name = request.form["user_name"]
    user = session2.query(User).filter_by(user_name=user_name).first()
    if user:
        password = request.form["password"]
        hashed_password = sha256((user_name + password + key.SALT).encode("utf-8")).hexdigest()
        if user.hashed_password == hashed_password:
            session["user_name"] = user_name
            return redirect(url_for("index"))
        else:
            return redirect(url_for("top", status="wrong_password"))
    else:
        return redirect(url_for("top", status="user_notfound"))


@app2.route("/registar", methods=["post"])
def registar():
    user_name = request.form["user_name"]
    user = session2.query(User).filter_by(user_name=user_name).first()
    if user:
        return redirect(url_for("user.newcomer", status="exist_user"))
    else:
        password = request.form["password"]
        hashed_password = sha256((user_name + password + key.SALT).encode("utf-8")).hexdigest()
        user = User(user_name, hashed_password)
        session2.add(user)
        session2.commit()
        #session["user_name"] = user_name
        return redirect(url_for("index"))


@app2.route("/logout")
def logout():
    session.pop("user_name", None)
    return redirect(url_for("top", status="logout"))


@app2.route("/newcomer")
def newcomer():
    status = request.args.get("status")
    return render_template("newcomer.html", status=status)


if __name__ == "__main__":
    app2.run(debug=True)