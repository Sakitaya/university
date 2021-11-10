#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
from datetime import datetime

import sqlalchemy
from flask import render_template, request, redirect, url_for, Blueprint, Flask, jsonify
from sqlalchemy.orm import scoped_session, sessionmaker
from app.session_change import order
from library.models.models.models_Beverages import Beverages
from library.models.models.models_User import User
from library.models.models.models_Orders import Orders, PastOrders
import json

app1 = Flask(__name__)
price = None
point = None
databese_file = os.path.join(os.path.abspath(os.path.dirname(__file__)), '../../library/models/models/Orders.db')
engine = sqlalchemy.create_engine('sqlite:///' + databese_file, convert_unicode=True)
session2 = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
all_order = session2.query(Orders).all()



@app1.route("/delete", methods=["post"])
def delete():
    data = json.loads(request.json)
    id_list = data["id_list"]
    databese_file = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                                 '../../library/models/models/Orders.db')
    engine = sqlalchemy.create_engine('sqlite:///' + databese_file, convert_unicode=True)
    session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
    for id in id_list:
        content = session.query(Orders).filter_by(id=id).first()
        session.delete(content)
    session.commit()
    return order()


@app1.route("/add", methods=["post"])
def add():
    data = json.loads(request.json)
    id = data["id"]
    if id is not None:
        databese_file = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                                     '../../library/models/models/Orders.db')
        engine = sqlalchemy.create_engine('sqlite:///' + databese_file, convert_unicode=True)
        session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

        title = data["title"]
        body = data["body"]
        price = data["price"]
        date = datetime.now()
        oo = Orders(title, body, price, date)
        session.add(oo)
        session.commit()
        return json.dumps({"messege": "suceeded!"})
    else:
        return json.dumps({"messege": "faild"})
    #return redirect(url_for("index"))


@app1.route("/set", methods=["post"])
def set():
    count = 0
    price = 0
    databese_file = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                                 '../../library/models/models/Orders.db')
    engine = sqlalchemy.create_engine('sqlite:///' + databese_file, convert_unicode=True)
    session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
    o_all_beverages = session.query(Orders).all()
    for beverages in o_all_beverages:
        order = int(beverages.price)
        price = price + order
        name = beverages.title
        count_zaiko(name)
    return json.dumps({"price": price})


def count_zaiko(name):
    databese_file = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                                 '../../library/models/models/Beverages.db')
    engine = sqlalchemy.create_engine('sqlite:///' + databese_file, convert_unicode=True)
    session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
    all_beverages = session.query(Beverages).all()
    for beverages in all_beverages:
        zaiko = int(beverages.zaiko)
        if name == beverages.title:
            zaiko = zaiko - 1
            beverages.zaiko = zaiko
            if int(beverages.zaiko) < 0:
                beverages.zaiko = 0
            session.commit()
    return 0


@app1.route("/set2")
def set_2():
    price = 0
    point = int(request.args.get("point"))
    databese_file = os.path.join(os.path.abspath(os.path.dirname(__file__)), '../../models/Orders.db')
    engine = sqlalchemy.create_engine('sqlite:///' + databese_file, convert_unicode=True)
    session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
    all_beverages = session.query(Orders).all()
    for beverages in all_beverages:
        order = int(beverages.price)
        price = price + order
        name = beverages.title
    price = price - point
    return render_template("set.html", price=price, all_beverages=all_beverages)

@app1.route("/pay", methods=["post"])
def pay():
    data = json.loads(request.json)
    points = data["point"]
    databese_file = os.path.join(os.path.abspath(os.path.dirname(__file__)), '../../library/models/models/User.db')
    engine = sqlalchemy.create_engine('sqlite:///' + databese_file, convert_unicode=True)
    session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
    all_user = session.query(User).all()
    for user in all_user:
        u_point = int(user.point)
        # if u_point <= 0:
        #     points = 0
        #     #return redirect(url_for("stock.set_2", point=points))
        # if u_point < points:
        #     points = 0
        #     return redirect(url_for("stock.set_2", point=points))
        u_point_int = u_point - points
        user.point = u_point_int
        user.used_point = points
        session.commit()
        name = user.user_name
        return json.dumps({"point": points})
        #return redirect(url_for("stock.set_2", point=points))


@app1.route("/failed", methods=["post"])
def failed():
    databese_file = os.path.join(os.path.abspath(os.path.dirname(__file__)), '../../library/models/models/User.db')
    engine = sqlalchemy.create_engine('sqlite:///' + databese_file, convert_unicode=True)
    session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
    all_user = session.query(User).all()
    for user in all_user:
        print("%s入りました。", user)
        used_point = user.used_point
        point = int(user.point) + used_point
        user.point = point
        user.used_point = None
        session.commit()
    for i in all_order:
        print("入りました")
        id = i.id
        datetime_before = i.date
        date_failed = datetime.now() - datetime_before
        all_past_order = session2.query(PastOrders).filter_by(id=id).first()
        for j in all_past_order:
            j.datetime_after = date_failed.total_seconds()
    return json.dumps({"status": "roll backed"})


if __name__ == "__main__":
    app1.run(debug=False, host='0.0.0.0', port=5000)