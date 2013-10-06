
import urllib
import urllib2
import cookielib
import logging
import logging.config

logging.config.fileConfig("logging.conf")
logger = logging.getLogger("logger_pixiv")
timeout = 100

class Pixiv():
	timeout = 100
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

	def login(self, proxy=False):
		self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookielib.LWPCookieJar()))
		# add proxy
		urllib2.install_opener(self.opener)
		data = urllib.urlencode(self.__login_data)
		# f = urllib2.urlopen(self.__urls["login"], data)
		f = self.opener.open(self.__urls["login"], data)
		if f.read().find(self.__static["login_success"]) != -1:
			return True
		else:
			return False

def main():
	p = Pixiv('mulvren@126.com', '11908298')
	print p.login()

if __name__ == '__main__':
	main()

		