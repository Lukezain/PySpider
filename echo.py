#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'Zain Luke'

#一个玩具,2015年7月份写完。后续没有测试是否可以持续使用。
#爬取echo回声
import  urllib.request 
import urllib.parse 
import  http.cookiejar
import re
import os
import time
import random
import socket
ISOTIMEFORMAT='%Y-%m-%d %X'
def login(q):
    x = q
    values={ 
            'login_form[name]':'your user-name', 
            'login_form[password]':'your password' 
    } 
    logUrl="http://www.app-echo.com/index/login" 
    cook=http.cookiejar.CookieJar() 
    openner=urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cook)) 
    openner.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36')] 
    r=openner.open(logUrl,urllib.parse.urlencode(values).encode()) 

    
    url = "http://www.app-echo.com/channel/1091?page=" + str(q)
    a = openner.open(url)
    data = a.read()
    a.close()
    data = data.decode("utf-8")
    redata = re.findall('<h3 class="voice-name"><a href="(.*?)">(.*?)</a></h3>',data,re.S)
    print ("第%d页载入成功\n" % q)
    n = []
    m = []
    for x in redata:
    #添加链接地址进入列表
        n.append(x[0])
    #添加铃声名字进入列表
        m.append(x[1])
    s = zip(n,m)
    print ("已经获得%d该页面所有链接地址" % q)
    return s
os.chdir("D:\\3D")
os.getcwd()
def download(s):
    w = 0
    for b,d in s:
    #循环链接，打开每个铃声页面

        try:
            w = w + 1
            soundurl = "http://www.app-echo.com" + str(b)
            c = urllib.request.urlopen(soundurl,timeout = 10)
            datas = c.read()
            c.close()
            print ("第%d个链接读入完成" % w)
            datas = datas.decode("utf-8")
            redatas = re.findall('play_source\("\d+".*?, "(http://.*?)"\);',datas,re.S)
            redatas = ''.join(redatas)
            funny = urllib.request.urlopen(redatas).read()
            try:
                f = open(d,'wb')
                f.write(funny)
                f.close
                print ("%s写入完成\n" % d)
            except OSError:
                f = open("1.txt",'w+')
                f.write(time.strftime(ISOTIMEFORMAT))      
                f.write("   发生第一个错误，该文件名应为：")
                f.write(d)
                f.write("\n\n")
                f.close
                print ("发生错误，已写入错误日志")
        except socket.timeout:
            print ("超时，已处理……")
        except urllib.error.HTTPError:
            print ("403错误，已处理")
        except:
            print ("发生未知错误")
            

            
        time.sleep(1)
    print ("写入完成")

page = 0
while page<433:
    page = page + 1
    download(login(page))
    t = random.randint(2,3)
    time.sleep(t)
