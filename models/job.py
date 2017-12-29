#!/usr/bin/env python
# -*- coding: utf-8 -*-

from peewee import *
from models import BaseModel

class Job(BaseModel):
    class Meta:
        db_table = "job"

    job_id = PrimaryKeyField()
    job_name = CharField(max_length=255)
    job_create_user = CharField(max_length=8)
    job_create_time = DateTimeField()
    display = IntegerField(default=1)
    results = TextField()
