
import urllib
import urllib2
import cookielib
import logging
import logging.config

logging.config.fileConfig("logging.conf")
logger = logging.getLogger("logger_pixiv")

class Pixiv():
	__urls = {
			"login": "http://www.pixiv.net/login.php"
	}

	__static = {
			"login_success": "pixiv.user.loggedIn = true"
	}

	def __init__(self, user, pwd):
		self.user = user
		self.pwd = pwd
		self.__login_data = {'mode':'login', 'pixiv_id':user, 'pass': pwd}

	def login(proxy=False):
		self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookielib.LWPCookieJar()))
		# add proxy
		data = urllib.urlencode(self.__login_data)
		f = opener.open(self.__urls["login"], data)
		if f.read().find(self.__static["login_success"]) != -1:
			return True
		else:
			return False

		