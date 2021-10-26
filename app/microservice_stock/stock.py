#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import sqlalchemy
from flask import render_template, request, redirect, url_for,  Blueprint
from sqlalchemy.orm import scoped_session, sessionmaker
from app.session_change import order
from library.models import Beverages
from library.models import Orders



app1 = Blueprint('stock', __name__, template_folder='../templates')

@app1.route("/order", methods=["post"])
def order():
    databese_file = os.path.join(os.path.abspath(os.path.dirname(__file__)), '../../library/models/models/Orders.db')
    engine = sqlalchemy.create_engine('sqlite:///' + databese_file, convert_unicode=True)
    session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
    all_beverages = session.query(Orders).all()
    return render_template("order.html",  all_beverages=all_beverages)


@app1.route("/delete", methods=["post"])
def delete():
    databese_file = os.path.join(os.path.abspath(os.path.dirname(__file__)), '../../library/models/models/Orders.db')
    engine = sqlalchemy.create_engine('sqlite:///' + databese_file, convert_unicode=True)
    session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
    all_beverages = session.query(Orders).all()
    id_list = request.form.getlist("delete")
    for id in id_list:
        content = session.query(Orders).filter_by(id=id).first()
        session.delete(content)
    session.commit()
    return order()

@app1.route("/add", methods=["post"])
def add():
    id_list = request.form.getlist("add")
    for id in id_list:
        #session = beverage()
        content = Beverages.query.filter_by(id=id).first()
        title = content.title
        body = content.body
        price = content.price
        databese_file = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                                     '../../library/models/models/Orders.db')
        engine = sqlalchemy.create_engine('sqlite:///' + databese_file, convert_unicode=True)
        session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
        oo = Orders(title, body, price)
        session.add(oo)
    session.commit()
    return redirect(url_for("index"))


@app1.route("/set", methods=["post"])
def set():
    price = 0
    databese_file = os.path.join(os.path.abspath(os.path.dirname(__file__)), '../../library/models/models/Orders.db')
    engine = sqlalchemy.create_engine('sqlite:///' + databese_file, convert_unicode=True)
    session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
    all_beverages = session.query(Orders).all()
    for beverages in all_beverages:
        order = int(beverages.price)
        price = price + order
        name = beverages.title
    return render_template("set.html", price=price, all_beverages=all_beverages)
    all_beverages = Beverages.query.all()
    for beverages in all_beverages:
        zaiko = int(beverages.zaiko)
        id = beverages.id
        if name == beverages.title:
            row = Beverages.query.get(id)
            zaiko = zaiko-1
            row.zaiko = zaiko
            db_session.commit()

if __name__ == "__main__":
    app1.run(debug=True, host='0.0.0.0', port=80)