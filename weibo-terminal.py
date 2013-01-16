#!/usr/bin/env python
# -*- coding: utf8 -*-
from lib import *
from time import *
import urllib2
import urllib
import json
import sys
import getpass
 

USERID = None
PASSWD = None 

IMPORTANT = ['小媛在努力_FightForCAS','豆子要排除干扰忠于初心']

if __name__ == "__main__":
    while True:
        USERID = raw_input("输入登录ID:")
        PASSWD = getpass.getpass("输入密码:")
        try:
            client = Weibo(USERID, PASSWD)
            break
        except APIError, e:
            print e
            continue
            
    wait_time = 3
    weibo_list = []
    love_weibos = []
    user_info = client.users__show(screen_name = 'cloudaice')
    uid = client.account__get_uid()['uid']
    count = 20

    while True:
        text = client.statuses.friends_timeline.get(count = count)
        for weibo in text['statuses']:
            in_text = ''
            tm = weibo['created_at']
            tm = tm.replace('+0800 ','')
            tm = int(mktime(strptime(tm)))
            name = weibo['user']['screen_name']
            post = weibo['text']
            if 'retweeted_status' in weibo:
                in_text = weibo['retweeted_status']['text']
            weibo_list.append((name,post,tm, in_text or ''))
        weibo_list = sorted(weibo_list, key = lambda d: d[2], reverse = True)
        while weibo_list:
            name, post, tm, in_text = weibo_list.pop()
            print strftime('%X',localtime(tm))
            print '%s' % name
            print '   %s' % post
            if in_text:
                print '      %s\n' % in_text 
            if name.encode('utf-8') in IMPORTANT:
                love_weibos.append((name, post, tm, in_text))
                sleep(5)
            sleep(wait_time)
        notice = client.remind__unread_count(uid = uid)
        while notice['status'] < 2:
            for name, post, tm, in_text in love_weibos:
                print strftime('%X',localtime(tm))
                print '%s' % name
                print '   %s' % post
                if in_text:
                    print '      %s\n' % in_text 
                sleep(wait_time)
            try:
                notice = client.remind__unread_count(uid = uid)
            except:
                notice = client.remind__unread_count(uid = uid)

        count = notice['status']
