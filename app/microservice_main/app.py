#!/usr/bin/python
# -*- coding: utf-8 -*-
import os

import sqlalchemy
from flask import render_template, session, url_for
from sqlalchemy.orm import scoped_session, sessionmaker

from models.models_Beverages import Beverages
from models.models_Orders import Orders
from app.microservice_main import key
from flask import Flask, redirect, request



app = Flask(__name__)
app.secret_key = key.SECRET_KEY

from app.microservice_stock.stock import app1
app.register_blueprint(app1)

from app.microservice_user.user import app2
app.register_blueprint(app2)

from app.microservice_main.payment import app3
app.register_blueprint(app3)

@app.route("/")
@app.route("/index")
def index():
    if "user_name" in session:
        name = session["user_name"]
        all_beverages = Beverages.query.all()
        return render_template("index.html", name=name, all_beverages=all_beverages)
    else:
        return redirect(url_for("top", status="logout"))


@app.route("/index", methods=["post"])
def post():
    if "user_name" in session:
        name = session["user_name"]
        all_beverages = Beverages.query.all()
        return render_template("index.html", name=name, all_beverages=all_beverages)
    else:
        return redirect(url_for("top", status="logout"))


@app.route("/top")
def top():
    status = request.args.get("status")
    return render_template("top.html",status=status)


@app.route("/clear", methods=['POST'])
def clear():
    databese_file = os.path.join(os.path.abspath(os.path.dirname(__file__)), '../../models/Orders.db')
    engine = sqlalchemy.create_engine('sqlite:///' + databese_file, convert_unicode=True)
    session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
    content = session.query(Orders).all()
    for i in content:
        session.delete(i)
        session.commit()
    return redirect(url_for("top", status="logout"))



if __name__ == "__main__":
    app.run(debug=True)