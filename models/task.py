#!/usr/bin/env python
# -*- coding: utf-8 -*-

from peewee import *
from models import BaseModel
from models.job import Job
from models.script import Script

class Task(BaseModel):
    class Meta:
        db_table = "task"

    task_id = PrimaryKeyField()
    task_name = CharField(max_length=16)
    timeout = IntegerField()
    hostname = CharField(max_length=16)
    job_id = IntegerField()
    script_id = IntegerField()
