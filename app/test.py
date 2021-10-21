#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, session, redirect, url_for
from models.models_Beverages import User, Beverages, Orders
from models.database import db_session
from datetime import datetime
from app import key
from hashlib import sha256
import sqlite3

for id in id_list:
    content = Beverages.query.filter_by(id=id).first()
    db_session.add(content)
db_session.commit()