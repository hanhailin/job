#!/usr/bin/env python
# -*- coding: utf-8 -*-

from peewee import *
from models import BaseModel

class Script(BaseModel):
    class Meta:
        db_table = "script"

    script_id = PrimaryKeyField()
    script_name = CharField(max_length=255)
    script_content = TextField()
    script_type = CharField(max_length=8)
