#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib, urllib2

def joblist(jumpserverurl, username, password):
    if not jumpserverurl:
        jumpserverurl = "http://172.16.100.50:8000/auths"

    values = {
        "username": username,
        "password": password
    }
    data = urllib.urlencode(values)
    req = urllib2.Request(jumpserverurl, data)
    response = urllib2.urlopen(req)
    return response.read()

def main():
    print authjumpserver('http://172.16.100.50:8000/auths', 'hanhailin')


if __name__ == "__main__":
    main()
