#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
import os
import random
from datetime import datetime
import numpy as np
import schedule
import sqlalchemy
from flask import render_template, request, redirect, url_for, Blueprint, Flask, jsonify
from library.models.models.models_User import User
from sqlalchemy.orm import scoped_session, sessionmaker


from models.models_payment import Payment, Used
import requests

from library.models.models.models_Beverages import Beverages
from library.models.models.models_Orders import Orders
app4 = Flask(__name__)

points: int
zaiko: int
blacklist: list
ca1: int = 0
ca2: int = 0
ca3: int = 0
work1: str
work2: str
work3: str
hyouka11: int = 0
hyouka12: int = 0
hyouka13: int = 0
hyouka21: int = 0
hyouka22: int = 0
hyouka23: int = 0
hyouka31: int = 0
hyouka32: int = 0
hyouka33: int = 0
advance_score = 0
normal_score = 0
choose: int = 0
choose_which = None
advance_choose = 0
normal_choose = 0
result = 2
ca1_level = 0
ca2_level = 0
ca3_level = 0
limit = 0
count = 0
id_list = None
user_cancel = 0
uketori_kyohi = 0
su_count = 0
fa_count = 0

@app4.route("/")
def kiri():
    global ca1, ca2, ca3, work1, work2, work3, choose, choose_which, points, advance_choose, normal_choose, result, limit, count, id_list, user_cancel, uketori_kyohi, su_count, fa_count
    count += 1
    point = np.random.choice(["0", "1"], p=[0.4, 0.6])
    point1 = str(point)
    points = int(point)
    limit = np.random.choice(["0", "1"], p=[0.0, 1.0])
    id_list = np.random.choice(["1", "2", "3"], p=[0.5, 0.5, 0.0])
    user_cancel = 0
    uketori_kyohi = 0
    su_count = 0
    fa_count = 0
    so = count % 10
    if so == 0:
        random_choice = np.random.choice(["0", "1", "2", "3"], p=[0.25, 0.25, 0.25, 0.25])
        random_choice = int(random_choice)
        if random_choice == 0:
            limit = np.random.choice(["0", "1"], p=[1, 0])
        if random_choice == 1:
            id_list = np.random.choice(["1", "2", "3"], p=[0, 0, 1])
        if random_choice == 2:
            user_cancel = 1
        if random_choice == 3:
            uketori_kyohi = 1
    # if count % 100 == 0:
    #     count_on = count // 100
    #     count_on = count_on % 2
    #     if count_on == 1:
    #         limit = np.random.choice(["0", "1"], p=[1, 0])
    #     if count_on == 0:
    #         id_list = np.random.choice(["1", "2", "3"], p=[0, 0, 1])
    payload = {"point": point1, "id_list": id_list, "limit": limit, "user_cancel": user_cancel, "uketori_kyohi": uketori_kyohi}
    work1 = worker1()
    work2 = worker2()
    work3 = worker3()
    # advance_choose = advance(ca1, ca2, ca3)
    # normal_choose = normal(ca1, ca2, ca3)
    # o = normal(ca1, ca2, ca3)
    cb1 = ca1
    cb2 = ca2
    cb3 = ca3
    advance_choose = advance(ca1, ca2, ca3)
    normal_choose = normal(cb1, cb2, cb3)
    if result == 1:
        o = advance(ca1, ca2, ca3)
    if result == 2:
        o = normal(ca1, ca2, ca3)
    else:
        o = normal(ca1, ca2, ca3)
    ave_ca = (ca1 + ca2 + ca3) / 3
    if ca1 > ave_ca:
        if work1 == "success":
            su_count += 1
        if work1 == "failed":
            fa_count += 1
    if ca2 > ave_ca:
        if work2 == "success":
            su_count += 1
        if work2 == "failed":
            fa_count += 1
    if ca3 > ave_ca:
        if work3 == "success":
            su_count += 1
        if work3 == "failed":
            fa_count += 1
    if advance_choose > 100:
        if ca1_level > 0:
            advance_choose -= ca1_level * 100
        if ca2_level > 0:
            advance_choose -= ca2_level * 100
        if ca3_level > 0:
            advance_choose -= ca3_level * 100
    if su_count > fa_count:
        o = "success"
    else:
        o = "failed"
    # if ca1 == o:
    #     if work1 == "success":
    #         choose = ca1
    #         choose_which = 1
    #         url = 'http://192.168.100.63:80'
    #         requests.get(url=url, json=json.dumps(payload))
    #     else:
    #         choose = ca1
    #         choose_which = 2
    #         url = 'http://192.168.100.63:81'
    #         requests.get(url=url, json=json.dumps(payload))
    # elif ca2 == o:
    #     if work2 == "success":
    #         choose = ca2
    #         choose_which = 1
    #         url = 'http://192.168.100.63:80'
    #         requests.get(url=url, json=json.dumps(payload))
    #     else:
    #         choose = ca2
    #         choose_which = 2
    #         url = 'http://192.168.100.63:81'
    #         requests.get(url=url, json=json.dumps(payload))
    # elif ca3 == o:
    #     if work3 == "success":
    #         choose = ca3
    #         choose_which = 1
    #         url = 'http://192.168.100.63:80'
    #         requests.get(url=url, json=json.dumps(payload))
    #     else:
    #         choose = ca3
    #         choose_which = 2
    #         url = 'http://192.168.100.63:81'
    #         requests.get(url=url, json=json.dumps(payload))
    # else:
    #     url = 'http://192.168.100.63:80'
    #     requests.get(url=url, json=json.dumps(points))
    if o == "success":
        choose_which = 1
        url = 'http://192.168.100.63:80'
        requests.get(url=url, json=json.dumps(payload))
    elif o == "failed":
        choose_which = 2
        url = 'http://192.168.100.63:81'
        requests.get(url=url, json=json.dumps(payload))
    return json.dumps({"status": "roll backed"})


@app4.route("/saga_failed", methods=["post"])
def saga_failed():
    global ca1, ca2, ca3, work1, work2, work3
    work1 = worker1()
    work2 = worker2()
    work3 = worker3()
    if work1 != "success":
        ca1 += 1
    if work1 == "success":
        ca1 -= 1
    if work2 != "success":
        ca2 += 1
    if work2 == "success":
        ca2 -= 1
    if work3 != "success":
        ca3 += 1
    else:
        ca3 -= 1
    if ca1 < 0:
        ca1 = 0
    if ca2 < 0:
        ca2 = 0
    if ca3 < 0:
        ca3 = 0
    return json.dumps({"status": "roll backed"})


@app4.route("/saga_success", methods=["post"])
def saga_success():
    global ca1, ca2, ca3, work1, work2, work3
    work1 = worker1()
    work2 = worker2()
    work3 = worker3()
    if work1 == "success":
        ca1 += 1
    elif work1 == "failed":
        ca1 -= 1
    if work2 == "success":
        ca2 += 1
    elif work2 == "failed":
        ca2 -= 1
    if work3 == "failed":
        ca3 -= 1
    elif work3 == "success":
        ca3 += 1
    if ca1 < 0:
        ca1 = 0
    if ca2 < 0:
        ca2 = 0
    if ca3 < 0:
        ca3 = 0
    return json.dumps({"status": "roll backed"})


@app4.route("/score", methods=["get"])
def score():
    global advance_score, normal_score, advance_choose, normal_choose
    data = json.loads(request.json)
    status = int(data)
    if advance_choose >= 100:
        if ca1_level > 0:
            advance_choose -= ca1_level * 100
        elif ca2_level > 0:
            advance_choose -= ca2_level * 100
        elif ca3_level > 0:
            advance_choose -= ca3_level * 100
    if status == 1:
        if choose == advance_choose:
            if choose_which == 1:
                advance_score += 1
        if choose == normal_choose:
            if choose_which == 1:
                normal_score += 1
    elif status == 102 or 103:
        if choose == advance_choose:
            if choose_which == 2:
                advance_score += 1
        if choose == normal_choose:
            if choose_which == 2:
                normal_score += 1
    return json.dumps({"status": "roll backed"})


def zai():
    global zaiko, id_list
    databese_file = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                                 '../../library/models/models/Beverages.db')
    engine = sqlalchemy.create_engine('sqlite:///' + databese_file, convert_unicode=True)
    session2 = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
    content_Bverages = session2.query(Beverages).all()
    databese_file = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                                 '../../library/models/models/Orders.db')
    engine = sqlalchemy.create_engine('sqlite:///' + databese_file, convert_unicode=True)
    session3 = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
    content_Orders = session3.query(Orders).all()
    id_list = int(id_list)
    for j in content_Bverages:
        # print(j.title)
        if id_list == j.id:
            # print("商品名一致")
            zaiko = int(j.zaiko)
    return zaiko




cancel_count = 0
def user():
    global blacklist
    databese_file = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                                 '../../library/models/models/User.db')
    engine = sqlalchemy.create_engine('sqlite:///' + databese_file, convert_unicode=True)
    session2 = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
    all_user = session2.query(User).all()
    for user in all_user:
        if "admin" in user.user_name:
            cancel_count = user.cancel_count
            if cancel_count > 500:
                blacklist = user.user_name
            return cancel_count


def worker1():
    global ca1, work1, points, hyouka11, hyouka12, hyouka13, points, limit, count
    limit = int(limit)
    if limit == 0:
        hyouka11 += 2
        hyouka12 += 1
        hyouka13 += 1
    else:
        hyouka11 += 1
        hyouka12 += 1
        hyouka13 += 1
    # if hyouka11 > 100:
    #     print("worker1リセットしました")
    #     hyouka11 = 1
    #     hyouka12 = 0
    #     hyouka13 = 0
    sum = hyouka11 - hyouka12
    if limit < sum:
        work1 = "success"
    else:
        work1 = "failed"
    return work1


def worker2():
    global hyouka21, hyouka22, hyouka23
    global ca2, work2
    zaiko = zai()
    if zaiko < 3:
        hyouka21 += 1
        hyouka22 += 2
        hyouka23 += 1
    else:
        hyouka21 += 1
        hyouka22 += 1
        hyouka23 += 1
    # if hyouka21 or hyouka22 or hyouka23 >= 100:
    #     print("worker2リセットしました")
    #     hyouka21 = 0
    #     hyouka22 = 0
    #     hyouka23 = 0
    sum = hyouka22 - hyouka21
    if zaiko <= sum:
        work2 = "failed"
    else:
        work2 = "success"
    return work2


def worker3():
    global ca3, work3, hyouka31, hyouka32, hyouka33, points
    cancel_count = user()
    if cancel_count > 100:
        hyouka31 += 1
        hyouka32 += 1
        hyouka33 += 2
    else:
        hyouka31 += 1
        hyouka32 += 1
        hyouka33 += 1
    # if hyouka31 or hyouka32 or hyouka33 >= 100:
    #     print("worker3リセットしました")
    #     hyouka31 = 0
    #     hyouka32 = 0
    #     hyouka33 = 0
    sum = hyouka33 - hyouka32
    if cancel_count > 100:
        work3 = "failed"
    else:
        work3 = "success"
    return work3


def advance(a1, a2, a3):
    global ca1, ca2, ca3, ca1_level, ca2_level, ca3_level
    if a1 >= 100:
        print("advanceリセットしました---------")
        ca1_level += 1
        ca1 = 1
        ca2 = 0
        ca3 = 0
    elif a2 >= 100:
        print("advanceリセットしました-------")
        ca2_level += 1
        ca1 = 0
        ca2 = 1
        ca3 = 0
    elif a3 >= 100:
        print("advanceリセットしました--------")
        ca3_level += 1
        ca1 = 0
        ca2 = 0
        ca3 = 1
    if ca1_level > 0:
        a1 += ca1_level * 100
    if ca2_level > 0:
        a2 += ca2_level * 100
    if ca3_level > 0:
        a3 += ca3_level * 100
    advance_max = max(a1, a2, a3)
    if advance_max == a1:
        advance_max -= ca1_level * 100
    if advance_max == a2:
        advance_max -= ca2_level * 100
    if advance_max == a3:
        advance_max -= ca3_level * 100
    return advance_max


def normal(a1, a2, a3):
    global ca1, ca2, ca3
    if a1 >= 100:
        print("----normalリセットしました----")
        ca1 = 1
        ca2 = 0
        ca3 = 0
    elif a2 >= 100:
        print("normalリセットしました-----------")
        ca1 = 0
        ca2 = 1
        ca3 = 0
    elif a3 >= 100:
        print("normalリセットしました----------")
        ca1 = 0
        ca2 = 0
        ca3 = 1
    return max(a1, a2, a3)

@app4.route("/change", methods=["get"])
def change():
    global result
    print("でた")
    if advance_score > normal_score:
        result = 1
    elif normal_score > advance_score:
        result = 2
    return json.dumps({"status": "roll backed"})


if __name__ == "__main__":
    app4.run(debug=True, host='0.0.0.0', port=5004)