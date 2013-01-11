#!/usr/bin/env python
# -*- coding: utf8 -*-
from weibo import APIClient
from weibo import APIError
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


IMPORTANT = ['小媛在努力_FightForCAS','豆子要排除干扰忠于初心']
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
    except APIError, e:
        print e

    client = APIClient(app_key=APP_KEY, app_secret=APP_SECRET, redirect_uri=CALLBACK_URL)
    r = client.request_access_token(code)
    access_token = r.access_token                     # 新浪返回的token
    expires_in = r.expires_in                         # token过期的UNIX时间
    client.set_access_token(access_token, expires_in)
    return client



if __name__ == "__main__":
    while True:
        USERID = raw_input("输入登录ID:")
        PASSWD = getpass.getpass("输入密码:")
        try:
            client = Weibo()
            break
        except APIError, e:
            continue
            
    wait_time = 0.1
    weibo_list = []
    love_weibos = []
    user_info = client.users__show(screen_name = 'cloudaice')
    uid = client.account__get_uid()['uid']
    count = 10

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
                sleep(1)
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
            notice = client.remind__unread_count(uid = uid)
        count = notice['status']
