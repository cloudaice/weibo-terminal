#!/usr/bin/env python
# -*- coding: utf8 -*-
from weibo import APIClient
import urllib2
import urllib
import json
import time
import sys
from time import *
import getpass
 

APP_KEY = '3302956248'
APP_SECRET = 'a3d8968cc21fd8115ad6e90994755cfc'
CALLBACK_URL = 'https://api.weibo.com/oauth2/default.html'
AUTH_URL = 'https://api.weibo.com/oauth2/authorize'
USERID = None
PASSED = None 

def Weibo():
    client = APIClient(app_key=APP_KEY, app_secret=APP_SECRET, redirect_uri=CALLBACK_URL)
    referer_url = client.get_authorize_url()
    #print "referer url is : %s" % referer_url

    cookies = urllib2.HTTPCookieProcessor()
    opener = urllib2.build_opener(cookies)
    urllib2.install_opener(opener)
 
    postdata = {"client_id": APP_KEY,
                "redirect_uri": CALLBACK_URL,
                "userId": USERID,
                "passwd": PASSWD,
                "isLoginSina": "0",
                "action": "submit",
                "response_type": "code",
             }
 
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; rv:11.0) Gecko/20100101 Firefox/11.0",
               "Host": "api.weibo.com",
               "Referer": referer_url
             }
 
    req  = urllib2.Request(url = AUTH_URL,
                           data = urllib.urlencode(postdata),
                           headers = headers
                    )
    try:
        resp = urllib2.urlopen(req)
        #print "callback url is : %s" % resp.geturl()
        code = resp.geturl()[-32:]
    except Exception, e:
        print e

    client = APIClient(app_key=APP_KEY, app_secret=APP_SECRET, redirect_uri=CALLBACK_URL)
    r = client.request_access_token(code)
    access_token = r.access_token                     # 新浪返回的token
    expires_in = r.expires_in                         # token过期的UNIX时间
    client.set_access_token(access_token, expires_in)
    return client

if __name__ == "__main__":
    while True:
        USERID = raw_input("输入微博帐户:")
        PASSWD = getpass.getpass("输入密码")
        try:
            client = Weibo()
            break
        except:
            continue
    wait_time = 5
    weibo_list = []
    while True:
        text = client.statuses.friends_timeline.get(count = 100)
        for weibo in text['statuses']:
            tm = weibo['created_at']
            tm = tm.replace('+0800 ','')
            tm = int(mktime(strptime(tm)))
            name = weibo['user']['screen_name']
            post = weibo['text']
            weibo_list.append((name,post,tm))
        weibo_list = sorted(weibo_list, key = lambda weibo: weibo[2], reverse=True)
        while weibo_list:
            name, post, tm = weibo_list.pop()
            print '%8s' % name
            print '   %s' % post
            print strftime('%X',localtime(tm))
            sleep(wait_time)
