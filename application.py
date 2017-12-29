#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import torndb
import tornado.web
import motor
from url import handlers
from models import session
from models.session import Session, SessionManager

from tornado.options import options

settings = dict(
    title=u"linmaochang",
    xsrf_cookies=False,
    cookie_secret="__TODO:0d692b519b44fmcac86a49740c67779aea7bd34910bfd5849687a2de029d1255",
    debug=True,
    template_path=os.path.join(os.path.dirname(__file__), "templates"),
    static_path=os.path.join(os.path.dirname(__file__), "static"),
    login_url='/login',
)


class Application(tornado.web.Application):
    def __init__(self):
        super(Application, self).__init__(handlers, **settings)
        self.db = torndb.Connection(
            host=options.mysql_host,
            database=options.mysql_database,
            user=options.mysql_user,
            password=options.mysql_password,
            max_idle_time=options.max_idle_time,
            time_zone=options.time_zone,
        )
        self.session_manager = session.SessionManager(options.redis_session_secret, options.redis_session_timeout,
                                    options.redis_host, options.redis_port, options.redis_pass, options.session_db)
