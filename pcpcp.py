#!/usr/bin/env python
# -*- coding:utf-8 -*-
import urllib2
import urllib
import cookielib

class Pixiv:
    user = "不动金"

    def Login(self): # 登陆Pixiv
        # cookies
        cookie_support= urllib2.HTTPCookieProcessor(cookielib.CookieJar())
        opener = urllib2.build_opener(cookie_support, urllib2.HTTPHandler)
        urllib2.install_opener(opener)

        # 填表单 http://www.pixiv.net/index.php
        postdata=urllib.urlencode({
            'mode':'login',
            'pass':"mulvren@126.com",
            'pixiv_id': "11908298",
        })

        headers = {
            'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'
        }

        req = urllib2.Request(
            url = 'http://www.pixiv.net/index.php',
            data = postdata,
            headers = headers
        )

        #发送请求
        urllib2.urlopen(req)
        print "login."

# 刚开始还写了个函数来验证登陆是否成功了（取得主页源代码，查找自己的用户名？），感觉是不是有更好的方法？

    def VerifyLogin(self):
        mypage = "http://www.pixiv.net/mypage.php"
        headers = {
            'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'         #print postdata
            }
        req = urllib2.Request(
            url = mypage,
            headers = headers
        )

        #发送请求
        source = urllib2.urlopen(req).read()
        if source.find(self.user) != -1:
            print "Verify> login success"
        else:
            print "Verify> login failed."

if __name__ == '__main__':
  p = Pixiv()
  p.Login()
  p.VerifyLogin()