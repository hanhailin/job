#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tornado.web
from peewee import JOIN
from .index import BaseHandler
import datetime, json
from .index import BaseHandler
from models.job import Job
from models.script import Script
from models.task import Task
from utils.ansible_interface import *
from utils.unicodeformat import unicodeformat

class NewTaskHandler(BaseHandler):
    # @powerd('ops', 'dev')
    # @tornado.web.authenticated
    def get(self):
        # projects = Project.select().order_by(Project.name.desc())
        # info = json.dumps([ i._data for i in projects ])
        # self.write(info)
        self.render('newTask.html')

    def post(self):
        jobname = self.get_argument('jobname', None)
        taskname = self.get_argument('taskname', None)
        scriptname = self.get_argument('scriptname', None)
        scripttype = self.get_argument('scripttype', None)
        scriptcontent = self.get_argument('scriptcontent', None).replace('\r\n', '\n')
        hostname = self.get_argument('hostname', None)
        timeout = self.get_argument('timeout', None)
        ##插入job表并查询id
        Job.insert(job_name=jobname, job_create_user = self.current_user, job_create_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")).execute()
        job_id = Job.get(Job.job_name == jobname).job_id
        ##插入script表并查询id
        Script.insert(script_name=scriptname, script_content=scriptcontent,script_type=scripttype).execute()
        script_id = Script.get(Script.script_name == scriptname).script_id
        ##插入task表
        Task.insert(task_name=taskname, hostname=hostname, timeout=timeout, job_id=job_id, script_id=script_id).execute()
        # self.redirect("/newTask")

class PublishHandler(BaseHandler):
    def get(self):
        self.render('publish.html')
