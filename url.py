#!/usr/bin/env python
# -*- coding: utf-8 -*-

from handler import IndexHandler, LoginHandle, LogoutHandler, NewTaskHandler, \
JobListHandler, JoblistApiHandler, PublishHandler, JobDetailHandler

handlers = [
    (r"/", IndexHandler),
    (r"/login", LoginHandle),
    (r"/logout", LogoutHandler),
    (r"/newTask", NewTaskHandler),
    (r"/joblist", JobListHandler),
    (r"/jobdetail", JobDetailHandler),
    (r"/api/joblist", JoblistApiHandler),
    (r"/publish", PublishHandler),
]
