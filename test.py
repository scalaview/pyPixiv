#!/usr/bin/env python
# -*- coding:gbk -*-

import urllib
import urllib2
import json
import cookielib


def wFile():
	url = "http://cdn-pixiv.lolita.tw/rankings/%s/pixiv_daily.json"
	r = urllib2.urlopen(url % "20130828")
	with open("data.txt", 'wb') as f:
		while True:
			tmp = r.read(10000)
			if not tmp : break
			f.write(tmp)
			f.flush()
			print tmp
	r.close()

def login():
	url = "http://www.pixiv.net/login.php"
	post = {"mode": "login",
					"pixiv_id": "mulvren@126.com",
					"pass": "11908298",
					"return_to": "/",
					"skip": "1"
	}
	post_data = urllib.urlencode(post)
	headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux i686; rv:8.0) Gecko/20100101 Firefox/8.0',
							'Referer': "http://www.pixiv.net/"
						}
	req  = urllib2.Request(
        url = url,
        headers = headers
    )
	opener = urllib2.build_opener()
	response = opener.open(req)  
	response.read()
	header = dict(response.headers)
	with open('login.html', 'w') as f:
		f.write(urllib2.urlopen(req).read())
	print header
	return header["set-cookie"]
	# r = urllib2.urlopen(req)
def main():
	cookie = login()
	print cookie
	data = None
	with open("data.txt", "r") as f:
		data = json.load(f)

	print "load file finish!"
	print data[0]["title"].encode("utf-8")
	print data[0]["url"].encode("utf-8")
	print data[0]["author"].encode("utf-8")
	print data[0]["img_url"].encode("utf-8")
	headers = {
	 	"Accept": "text/plain",
		'Accept-Language':	'zh-cn,zh;q=0.8,en-us;q=0.5,en;q=0.3',
		'Connection':	'keep-alive',
		'Cookie':	cookie+"; PHPSESSID=81379b5bfdd7b300e0623e64757ef714",
		'Referer':	'http://www.pixiv.net/',
		'User-Agent':	'Mozilla/5.0 (Windows NT 6.2; rv:23.0) Gecko/20100101 Firefox/23.0'
	}
	s = data[0]["url"].encode("utf-8").replace("medium", "big").encode("utf-8")
	print s
	end = s.rindex("&")
	url2 = s[0: end]
	print url2
  # print url2

	# req  = urllib2.Request(
 #        url = url2,
 #        headers = headers
 #    )
	# r = urllib2.urlopen(req)
	# print r.read()
	# with open('req.html', 'w') as f:
	# 	f.write(r.read())
	# print r.geturl()
	# r.close()


# def get_file_size(url, proxy=None):  
# 		opener = urllib2.build_opener()  
# 		if proxy:  
# 		    if url.lower().startswith('https://'):  
# 		        opener.add_handler(urllib2.ProxyHandler({'https' : proxy}))  
# 		    else:  
# 		        opener.add_handler(urllib2.ProxyHandler({'http' : proxy}))  
# 		request = urllib2.Request(url)  
# 		request.get_method = lambda: 'HEAD'  
# 		try:  
# 		    response = opener.open(request)  
# 		    response.read()  
# 		except Exception, e:  
# 		    print '%s %s' % (url, e)  
# 		else:  
# 		    return dict(response.headers).get('content-length', 0) 

def logind(useproxy=False, proxyip=None, addr="http://www.pixiv.net/member_illust.php?mode=big&illust_id=38074857"):
	logindata={'mode':'login', 'pixiv_id':'yorkfinechan@gmail.com', 'pass':'cxhcxh'}
	opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookielib.LWPCookieJar()))
	if useproxy:
	        proxy_support = urllib2.ProxyHandler({'http':proxyip})
	        opener.add_handler(proxy_support)
	data = urllib.urlencode(logindata)
	opener.addheaders = [('Referer', r'http://www.pixiv.net/member_illust.php?mode=medium&illust_id=38108907')]
	f = opener.open('http://www.pixiv.net/login.php', data)
	if f.read().find('pixiv.user.loggedIn = true') != -1:
	        print u'success'

	        try:
							opener.addheaders = [('Referer', r'http://www.pixiv.net/member_illust.php?mode=medium&illust_id=38074857')]
							f = opener.open(addr)
	        except urllib2.URLError as e:
	                print (u'net error:' + e.reason.__str__())
	        else:
	                print u'int'
	                htmlcode = f.read()
	                f.close()
	        if htmlcode != None:
	                return htmlcode
	else:
	        print u'fail'
	        return None

if __name__ == '__main__':
	wFile()
	# main()
	# login()
	# with open('g.html', 'w') as f:
	# 	f.write(logind())