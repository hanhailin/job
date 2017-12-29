#!/usr/bin/env python
# -*- coding: utf-8 -*-

def unicodeformat(input):
    if isinstance(input, dict):
        return {unicodeformat(key): unicodeformat(value) for key, value in input.iteritems()}
    elif isinstance(input, list):
        return [unicodeformat(element) for element in input]
    elif isinstance(input, unicode):
        return input.encode('utf-8')
    else:
        return input
