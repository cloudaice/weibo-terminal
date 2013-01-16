#!/usr/bin/env python
# -*- coding: utf8 -*-
from weibo import *
import urllib2
from lib import *
import sys
reload(sys)
sys.setdefaultencoding('utf8')
USERID = None
PASSWD = None 

if __name__ == "__main__":
    while True:
        USERID = raw_input("输入登录ID:")
        PASSWD = getpass.getpass("输入密码:")
        try:
            client = Weibo(USERID, PASSWD)
            break
        except APIError, e:
            continue

    while True:
        weibo = raw_input('>')
        if weibo == 'q':
            exit()
        try:
            weibo = client.statuses.update.post(status = weibo)
        except APIError, e:
            print e
            print '内容 %s 未发送！！！' % weibo['text']
            continue
        print '内容 %s 已经发送' % weibo['text']

