#!/usr/bin/env python
# -*- coding: utf-8 -*-

from peewee import *
from setting import mysql_db

db = MySQLDatabase(mysql_db['name'], host=mysql_db['host'], user=mysql_db['user'], passwd=mysql_db['pswd'],
                   port=mysql_db['port'], charset=mysql_db['charset'])


class BaseModel(Model):
    class Meta:
        database = db
        database.get_conn().ping(True)
