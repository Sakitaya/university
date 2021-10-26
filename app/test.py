#!/usr/bin/python
# -*- coding: utf-8 -*-
from library.models import Beverages
from library.models.models.database import db_session

for id in id_list:
    content = Beverages.query.filter_by(id=id).first()
    db_session.add(content)
db_session.commit()