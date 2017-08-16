#!/usr/bin/env python

#author     : Neil Zhang
#email      : neilzhangy@gmail.com
#version    : 1.1

#----change logs----
#
#
# 2017-08-16    v1.1    Done.


import HTMLParser  
import urlparse  
import urllib  
import urllib2  
import cookielib  
import string  
import sys
import re

LOGIN_REQUEST_HEADER = {
    'Host': '192.168.1.1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
    'Accept-Encoding': 'gzip, deflate',
    'Referer': 'http://192.168.1.1/',
    'Cookie': 'username=telecomadmin; password=nE7jA%5m',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1'
}

MNG_REQUEST_HEADER = {
    'Host': '192.168.1.1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
    'Accept-Encoding': 'gzip, deflate',
    'Referer': 'http://192.168.1.1/main.html?from=loginpage',
    'Cookie': '',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1'
}

REBOOT_REQUEST_HEADER = {
'Host': '192.168.1.1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
    'Accept-Encoding': 'gzip, deflate',
    'Referer': 'http://192.168.1.1/',
    'Referer': 'http://192.168.1.1/mng_resetrouter.html',
    'Cookie': '',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1'
}

host_url = 'http://192.168.1.1/login.html'

mng_url = 'http://192.168.1.1/mng_resetrouter.html'

reboot_url = 'http://192.168.1.1/mng_rebootinfoCN.cgi?sessionKey='

if __name__ == '__main__':
    #set cookies
    cj = cookielib.LWPCookieJar()  
    cookie_support = urllib2.HTTPCookieProcessor(cj)
    #install opener
    opener = urllib2.build_opener(cookie_support, urllib2.HTTPHandler)  
    urllib2.install_opener(opener)
    #open login url
    request = urllib2.Request(host_url, headers=LOGIN_REQUEST_HEADER)  
    response = urllib2.urlopen(request)
    #print response.read()
    #get session id
    session_id = 0
    for index, cookie in enumerate(cj):
        if cookie.name == 'sessionid':
            session_id = cookie.value
    if session_id == 0:
        print 'Login failed.'
        sys.exit(1)        
    print 'session id: ' + session_id
    #prepare header with session id
    MNG_REQUEST_HEADER['Cookie'] = 'language=cn; username=telecomadmin; password=nE7jA%5m; sessionid=' + session_id
    REBOOT_REQUEST_HEADER['Cookie'] = 'language=cn; username=telecomadmin; password=nE7jA%5m; sessionid=' + session_id
    #open management url
    request = urllib2.Request(mng_url, headers=MNG_REQUEST_HEADER)
    response = urllib2.urlopen(request)
    #print response.getcode()
    session_key = 0
    data = response.read()
    #print data
    #get session key
    m = re.search(r'sessionKey=\'(\d+)\'', data)
    if m:
        session_key = m.group(1)
    if session_key == 0:
        print 'Get session key failed.'
        sys.exit(1)
    print 'session key: ' + session_key
    #print response.read()
    #open reboot url
    reboot_url = reboot_url + session_key
    request = urllib2.Request(reboot_url, headers=REBOOT_REQUEST_HEADER)
    response = urllib2.urlopen(request)
    if 200 == response.getcode():
        print 'Reboot successfully done.'
    else:
        print 'Reboot failed.'   
    
    sys.exit(0)
