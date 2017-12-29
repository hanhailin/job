#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.autoreload
from tornado.options import define, options
from application import Application
from setting import mysql_db, redis_db

define("port", default=30001, help="run on the given port", type=int)

define("mysql_host", default="%s:%s" % (mysql_db['host'], mysql_db['port']))
define("mysql_database", default=mysql_db['name'])
define("mysql_user", default=mysql_db['user'])
define("mysql_password", default=mysql_db['pswd'])

define("redis_host", default=redis_db['redis_host'])
define("redis_port", default=redis_db['redis_port'])
define("redis_pass", default=redis_db['redis_pass'])
define("redis_session_secret", default="%s" % (redis_db['session_secret']))
define("redis_session_timeout", default="%s" % (redis_db['session_timeout']))
define("session_db", default=redis_db['session_db'])

define("max_idle_time", default=10)
define("time_zone", default="+8:00")

def main():
    reload(sys)                         # 2
    sys.setdefaultencoding('utf-8')
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application(), xheaders=True)
    http_server.listen(options.port)
    instance = tornado.ioloop.IOLoop.instance()
    tornado.autoreload.start(instance)
    instance.start()


if __name__ == "__main__":
    main()
