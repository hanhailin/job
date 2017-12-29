#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tornado.web
from .index import BaseHandler
from models import session

import sys
sys.path.append("..")
from utils.auths import authjumpserver

class LoginHandle(BaseHandler):
    def get(self):
        self.render('login.html', error=None)

    def post(self):
        URL = "http://172.16.100.50:8000/auths"
        code = authjumpserver(URL, self.get_argument('username'), self.get_argument('password'))
        if code == '10090':
            self.session["username"] = self.get_argument('username')
            self.session.save()
            self.redirect(self.get_argument('next', '/'))
        elif code == '10091':
            self.write('已经认证!')
        elif code == '10092':
            self.write('get账号无效，请联系管理员!')
        elif code == '10093':
            self.write('用户未激活，请联系管理员!')
        elif code == '10094':
            self.write('账号或密码错误，请联系管理员!')
        elif code == '10095':
            self.write('账号或密码错误，请联系管理员!')
        else:
            self.write('账号无效，请联系管理员!')
        print code

class LogoutHandler(BaseHandler):
    # @tornado.web.authenticated
    def get(self):
        self.session["username"] = None
        self.session.save()
        self.redirect(self.get_argument("next", "/login"))
