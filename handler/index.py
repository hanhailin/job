#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tornado.web
import functools

from models import db
from models import session
from models.session import SessionManager, Session, InvalidSessionException


class BaseHandler(tornado.web.RequestHandler):
    def __init__(self, *args, **kwargs):
        super(BaseHandler, self).__init__(*args, **kwargs)
        self.session = session.Session(self.application.session_manager, self)


    @property
    def db(self):
        return self.application.db

    @property
    def mongo(self):
        return self.application.mongo

    def get_current_user(self):
        username = self.session.get("username")
        if not username:
            return None
        # user_name = User.get(User.id == int(user_id))
        return username

    # def set_current_user(self):
    #     import time
    #     self.set_secure_cookie('user_id', '1', expires=time.time() + 900)

    def prepare(self):
        if not db.is_closed():
            db.close()
        db.connect()
        return super(BaseHandler, self).prepare()

    def on_finish(self):
        if not db.is_closed():
            db.close()
        return super(BaseHandler, self).on_finish()


class IndexHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        # if self.session['info'][1]['roles'] == 'bee':
        #     self.render('bee.html', error=None)
        # self.render('lte-index.html', error=None)
        # self.write('hello, welcome to my site!')
        self.render('base.html', error=None)


def powerd(*L):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(self, *args, **kw):
            if self.session['info'][1]['roles'] not in L:
                self.redirect(self.get_argument('next', '/'))
            return func(self, *args, **kw)
        return wrapper
    return decorator
