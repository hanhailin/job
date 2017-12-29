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

class JobListHandler(BaseHandler):
    def get(self):
        self.render('joblist.html')


class JoblistApiHandler(BaseHandler):
    def get(self):
        results = Job.select(Job.job_name, Job.job_create_time, Job.job_create_user, Job.display)
        data = [{"job_name": b.job_name, "job_create_user": b.job_create_user, "job_create_time": b.job_create_time.strftime("%Y-%m-%d %H:%M:%S"), "display": b.display} for b in results if b.display == 1]
        self.write(json.dumps(data))

    def post(self):
        jobname = self.get_argument('jobname', None)
        action = self.get_argument('action', None)
        if (action == "hiddenjob"):
            Job.update(display=0).where(Job.job_name == jobname).execute()
            self.write(json.dumps(dict({'code': '0'})))

        if (action == "startjob"):
            job_id = Job.get(Job.job_name == jobname).job_id
            jobdetail = Job.select(Job, Task).join(Task, JOIN.LEFT_OUTER, on=(Job.job_id == Task.job_id)).where(Job.job_name==jobname)

            jobdetail = [ {'hostname': i.job_id.hostname, 'taskid': i.job_id.task_id, 'scriptid': i.job_id.script_id} for i in jobdetail ]
            scriptid = jobdetail[0]['scriptid']
            scriptdetail = Script.select().where(Script.script_id == scriptid)
            for j in scriptdetail:
                jobdetail[0]['scriptcontent'] = j.script_content
                jobdetail[0]['scriptname'] = j.script_name
                jobdetail[0]['scripttype'] = j.script_type
            if (jobdetail[0]['scripttype'] == 'shell'):
                filename = jobdetail[0]['scriptname'] + '.sh'
            elif (jobdetail[0]['scripttype'] == 'python'):
                filename = jobdetail[0]['scriptname'] + '.py'
            elif (jobdetail[0]['scripttype'] == 'js'):
                filename = jobdetail[0]['scriptname'] + '.js'
            else :
                filename = jobdetail[0]['scriptname']
            with open('/tmp/' + filename, 'w') as f:
                f.write(jobdetail[0]['scriptcontent'])

        sourcefile = '/tmp/' + filename
        dest = '/root/'
        destfile = dest + filename
        req = urllib2.Request('http://172.16.100.50/jasset/asset/inventory/')
        response = urllib2.urlopen(req)
        resource = unicodeformat(json.loads(response.read()))['invernory']
        interface = AnsiInterface(resource)

        hosts = jobdetail[0]['hostname']
        try:
            interface.copy_file(hosts, src=sourcefile, dest=dest)
            interface.exec_script(hosts, '/bin/bash %s'%(destfile))
            recode = {'code': 0}
            self.write(json.dumps(recode))
        except:
            results = []
            recode = {'code': 101}
            self.write(json.dumps(recode))

class JobDetailHandler(BaseHandler):
    def get(self):
        self.render('jobdetail.html')
