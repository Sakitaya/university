#!/usr/bin/python
# -*- coding: utf-8 -*-
from models.models_Beverages import Beverages
from models.database import db_session

for id in id_list:
    content = Beverages.query.filter_by(id=id).first()
    db_session.add(content)
db_session.commit()