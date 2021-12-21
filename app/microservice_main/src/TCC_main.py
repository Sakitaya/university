#!/usr/bin/python
# -*- coding: utf-8 -*-
#001=Saga_Success
# 002 = Saga_failed
# 003 = TCC_Success
# 004 = TCC_failed
import os
import random
import time
from datetime import datetime

import numpy as np
import sqlalchemy
import requests
from flask import render_template, session, url_for
from sqlalchemy.orm import scoped_session, sessionmaker
from library.models.models.models_Beverages import Beverages
from library.models.models.models_Orders import Orders, PastOrders
from library.models.models.models_User import User
from library.models.models.models_payment import Payment
from app.microservice_main.src import key
from flask import Flask, redirect, request
import json
import numpy


app = Flask(__name__, template_folder='../../templates')
databese_file = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                                 '../../../library/models/models/Orders.db')
engine = sqlalchemy.create_engine('sqlite:///' + databese_file, convert_unicode=True)
session3 = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
status = None

@app.route("/")
def au():
    data = json.loads(request.json)
    point = int(data["point"])
    id_list = data["id_list"]
    limit = int(data["limit"])
    user_cancel = int(data["user_cancel"])
    uketori_kyohi = int(data["uketori_kyohi"])
    global status
    # reset()
    clear()
    add(id_list)
    set()
    pay(point)
    if point == 0:
        set_2(point, limit)
        status = checkout(user_cancel, uketori_kyohi)
        return json.dumps({"status": "roll backed"})
    else:
        set_2(point, limit)
        status = checkout(user_cancel, uketori_kyohi)
    score(status)
    return json.dumps({"status": "roll backed"})





def score(status):
    url = 'http://192.168.100.63:5004/score'
    requests.get(url=url, json=json.dumps(status))

def success():
    #url = 'http://192.168.100.63:5005/success'
    url = 'http://192.168.100.63:5006/success'
    res_failed = requests.post(url=url)
    return "2"

def reset():
    url = 'http://192.168.100.63:5006/reset'
    #url = 'http://192.168.100.63:5006/reset'
    res_failed = requests.post(url=url)
    return 0

def route():
    return render_template("top.html")


@app.route("/index")
def index():
    global status
    status = request.args.get("status")
    messege = request.args.get("messege")
    #session = request.args.get("session")
    #all_users = session.query(User.user_name).all()
    # if "user_name" in session:
    #     name = "admin"
    #     payload = {"name":name}
    #     res_user = requests.post(url=url, json=json.dumps(payload))
    #     databese_file = os.path.join(os.path.abspath(os.path.dirname(__file__)),
    #                                  '../../../library/models/models/Beverages.db')
    #     engine = sqlalchemy.create_engine('sqlite:///' + databese_file, convert_unicode=True)
    #     session1 = scoped_session(sessionmaker(autocommit=False, autoflush=True, bind=engine))
    #     all_beverages = session1.query(Beverages).all()
    #     #res = requests.post('192.168.100.63:5000/order', name=name, all_beverages=all_beverages)
    #     return render_template("index.html", name=name, all_beverages=all_beverages)
    # else:
    #     # databese_file = os.path.join(os.path.abspath(os.path.dirname(__file__)),'../../../library/models/models/Beverages.db')
    #     # engine = sqlalchemy.create_engine('sqlite:///' + databese_file)
    #     # session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
    #     # all_beverages = session.query(Beverages).all()
    #     #res = requests.post('192.168.100.63:5000/order', name=name, all_beverages=all_beverages)
    #     #return render_template("index.html", name=user_name, all_beverages=all_beverages)
    if status is not None:
        if "logout" in status:
            return redirect(url_for("top", status="logout"))
        else:
            databese_file = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                                         '../../../library/models/models/Beverages.db')
            engine = sqlalchemy.create_engine('sqlite:///' + databese_file)
            session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
            all_beverages = session.query(Beverages).all()
            return render_template("index.html", all_beverages=all_beverages)
    else:
        print("status is None")
    if "suceeded!" in messege:
        print("succes!")
        databese_file = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                                     '../../../library/models/models/Beverages.db')
        engine = sqlalchemy.create_engine('sqlite:///' + databese_file)
        session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
        all_beverages = session.query(Beverages).all()
        return render_template("index.html", all_beverages=all_beverages)




@app.route("/login", methods=["post"])
def login():
    global status
    url = 'http://192.168.100.63:5007/login'
    #url = 'http://192.168.100.63:5007/login'
    user_name = request.form["user_name"]
    password = request.form["password"]
    #user_name = "admin"
    payload = {"name":user_name, "password":password}
    res_user = requests.post(url=url, json=json.dumps(payload))
    info_status = json.loads(res_user.text)
    return redirect(url_for("index", status=info_status))


@app.route("/newcomer")
def newcomer():
    global status
    status = request.args.get("status")
    return render_template("newcomer.html", status=status)


@app.route("/registar", methods=["post"])
def registar():
    global status
    url = "http://192.168.100.63:5001/registar"
    #url = 'http://192.168.100.63:5001/registar'
    user_name = str(request.form["user_name"])
    password = str(request.form["password"])
    payload = {"name": user_name, "password": password}
    res = requests.post(url=url, json=json.dumps(payload))
    r = res.headers
    resjson = res.text
    #return redirect(url_for("newcomer", status="exist_user"))
    return redirect(url_for("top", status="succes"))

@app.route("/index", methods=["post"])
def post():
    return redirect(url_for("index", status="login"))

@app.route("/pay", methods=["post"])
def pay(point):
    global status
    #url = 'http://192.168.100.63:5009/pay'
    url = 'http://192.168.100.63:5009/pay'
    #points = int(request.form["point"])
    # point = random.randint(0, 1)
    payload = {"point": point}
    res_pay = requests.post(url=url, json=json.dumps(payload))
    info_point = json.loads(res_pay.text)
    return info_point
    #return redirect(url_for("set_2", point=points))

price = 0
@app.route("/set2")
def set_2(point, limit):
    global status, price
    if point != 0:
        #point = int(request.args.get("point"))
        databese_file = os.path.join(os.path.abspath(os.path.dirname(__file__)), '../../../library/models/models/Orders.db')
        engine = sqlalchemy.create_engine('sqlite:///' + databese_file, convert_unicode=True)
        session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
        all_beverages = session.query(Orders).all()
        for beverages in all_beverages:
            price = 0
            order = int(beverages.price)
            price = price + order
        price = price - point
        print("送ります")
    #url = 'http://192.168.100.63:5006/payment'
    url = "http://192.168.100.63:5006/payment"
    payload = {"price": price, "limit": limit}
    res_payment = requests.post(url=url, json=json.dumps(payload))
    info_payment = json.loads(res_payment.text)
    status = info_payment["status"]
    return 0
    #return render_template("set2.html", price=price, all_beverages=all_beverages)



@app.route("/top")
def top():
    global status
    status = request.args.get("status")
    if status == "failed":
        return redirect(url_for("failed"))
    else:
        return render_template("top.html", status=status)


@app.route("/logout")
def logout():
    return redirect(url_for("top", status="logout"))

@app.route("/add", methods=["post"])
def add(id_list):
    global status
    #id_list = request.form.getlist("add")
    #url = 'http://192.168.100.63:5009/add'
    url = "http://192.168.100.63:5009/add"
    for id in id_list:
        databese_file = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                                     '../../../library/models/models/Beverages.db')
        engine = sqlalchemy.create_engine('sqlite:///' + databese_file)
        session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
        content = session.query(Beverages).filter_by(id=id).first()
        title = content.title
        body = content.body
        price = content.price
        payload = {"id": id, "title": title, "body": body, "price": price}
        res_order = requests.post(url=url, json=json.dumps(payload))
    info_status = json.loads(res_order.text)
    messege = info_status["messege"]
    if "suceeded!" in messege:
        return 0
        #return redirect(url_for("index", messege=messege))
    else:
        return 0
        #return redirect(url_for("index", messege=messege))


@app.route("/order", methods=["post"])
def order():
    global status
    databese_file = os.path.join(os.path.abspath(os.path.dirname(__file__)), '../../../library/models/models/Orders.db')
    engine = sqlalchemy.create_engine('sqlite:///' + databese_file, convert_unicode=True)
    session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
    all_beverages = session.query(Orders).all()
    return render_template("order.html",  all_beverages=all_beverages)

@app.route("/delete", methods=["post"])
def delete():
    global status
    #url = 'http://192.168.100.63:5000/delete'
    url = 'http://192.168.100.63:5000/delete'
    id_list = request.form.getlist("delete")
    payload = {"id_list": id_list}
    res_user = requests.post(url=url, json=json.dumps(payload))
    return order()

@app.route("/set", methods=["post"])
def set():
    global status
    #url = 'http://192.168.100.63:5009/set'
    url = 'http://192.168.100.63:5009/set'
    payload = {"name": "data"}
    res_set = requests.post(url=url)
    info_set = json.loads(res_set.text)
    price = int(info_set["price"])
    zaiko = int(info_set["zaiko"])
    # url = 'http://192.168.100.63:5004/zai'
    # payload = {"zaiko": zaiko}
    # requests.post(url=url, json=json.dumps(payload))
    databese_file = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                                 '../../../library/models/models/Orders.db')
    engine = sqlalchemy.create_engine('sqlite:///' + databese_file, convert_unicode=True)
    session1 = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
    all_beverages = session1.query(Orders).all()
    databese_file = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                                 '../../../library/models/models/User.db')
    engine = sqlalchemy.create_engine('sqlite:///' + databese_file, convert_unicode=True)
    session2 = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
    content = session2.query(User).all()
    u_point = 0
    for i in content:
        if i.user_name in 'admin':
            u_point = i.point
        elif i.user_name in 'akitaya':
            u_point = i.point
    return zaiko
    #return render_template("set.html", price=price, all_beverages=all_beverages, u_point=u_point)


@app.route("/checkout", methods=['POST'])
def checkout(user_cancel, uketori_kyohi):
    global status
    name = None
    databese_file = os.path.join(os.path.abspath(os.path.dirname(__file__)), '../../../library/models/models/Beverages.db')
    engine = sqlalchemy.create_engine('sqlite:///' + databese_file, convert_unicode=True)
    session2 = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
    content_Bverages = session2.query(Beverages).all()
    content_Orders = session3.query(Orders).all()
    for i in content_Orders:
        name = i.title
        for j in content_Bverages:
            if i.title == j.title:
                zaiko = int(j.zaiko)
                if zaiko <= 0:
                    status = "zaiko_failed"
                else:
                    print("")
            else:
                print("商品名非一致")
    # for i in content_Orders:
    #     #print(i.title)
    #     for j in content_Bverages:
    #         #print(j.title)
    #         if i.title == j.title:
    #             #print("商品名一致")
    #             zaiko = int(j.zaiko)
    #             if zaiko == 0:
    #                 print("在庫なし")
    #                 status = "zaiko_failed"
    #             else:
    #                 print("在庫あり")
    #                 #status = "Success"
    #         else:
    #             print("商品名非一致")
    databese_file = os.path.join(os.path.abspath(os.path.dirname(__file__)), '../../../library/models/models/Payment.db')
    engine = sqlalchemy.create_engine('sqlite:///' + databese_file, convert_unicode=True)
    session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
    content2 = session.query(Payment).all()
    for limit in content2:
        if limit.limit <= 0:
            status = "payment_failed"
        else:
            print("")
            # status = "Success"
    databese_file = os.path.join(os.path.abspath(os.path.dirname(__file__)), '../../../library/models/models/Orders.db')
    engine = sqlalchemy.create_engine('sqlite:///' + databese_file, convert_unicode=True)
    session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
    content = session.query(Orders).all()
    if status == "zaiko_failed":
        url = 'http://192.168.100.63:5004/saga_failed'
        res = requests.post(url=url)
        status = "102"
        print("")
        for i in content:
            datetime_before = i.date
            date = datetime.now() - datetime_before
            title = i.title
            oo = PastOrders(title=title, status=status, date_after=date.total_seconds())
            session.add(oo)
            session.commit()
    elif status == "payment_failed":
        url = 'http://192.168.100.63:5004/saga_failed'
        res = requests.post(url=url)
        print("")
        status = "103"
        for i in content:
            datetime_before = i.date
            date = datetime.now() - datetime_before
            title = i.title
            oo = PastOrders(title=title, status=status, date_after=date.total_seconds())
            session.add(oo)
            session.commit()
    else:
        status = success()
        # session.delete(i)
        # session.commit()
    if user_cancel == 1:
        url = 'http://192.168.100.63:5004/saga_failed'
        res = requests.post(url=url)
        print("")
        status = "104"
        for i in content:
            datetime_before = i.date
            date = datetime.now() - datetime_before
            title = i.title
            oo = PastOrders(title=title, status=status, date_after=date.total_seconds())
            session.add(oo)
            session.commit()
    if uketori_kyohi == 1:
        url = 'http://192.168.100.63:5004/saga_failed'
        res = requests.post(url=url)
        print("")
        status = "105"
        for i in content:
            datetime_before = i.date
            date = datetime.now() - datetime_before
            title = i.title
            oo = PastOrders(title=title, status=status, date_after=date.total_seconds())
            session.add(oo)
            session.commit()
    return status
    #return redirect(url_for("top", status=status))


def clear():
    databese_file = os.path.join(os.path.abspath(os.path.dirname(__file__)), '../../../library/models/models/Orders.db')
    engine = sqlalchemy.create_engine('sqlite:///' + databese_file, convert_unicode=True)
    session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
    content = session.query(Orders).all()
    for i in content:
        session.delete(i)
        session.commit()
    return 0


@app.route("/failed")
def failed():
    #url = 'http://192.168.100.63:5001/failed'
    url = 'http://192.168.100.63:5001/failed'
    res_failed = requests.post(url=url)
    return 0
    #return render_template("top.html", status="roll backed")

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=81)
