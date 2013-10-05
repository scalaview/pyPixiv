

import time
import urllib2
import json
import Pixiv

def bind_api(path, date, dtype, host="http://cdn-pixiv.lolita.tw/rankings/%s/%s.%s"):

	class Method(object):
		def __init__(self):
			self.__url = host % (date, path, dtype)
			self.log = Pixiv.logger

		def execute(self):
			data = {}	
			try:
				tmpdata =[]
				self.log.info("open url: %s" % self.__url)
				res = urllib2.urlopen(self.__url)
				while True:
					tmp = res.read(1000)
					print tmp
					if not tmp: break
					tmpdata.append(tmp)
				data = json.dumps(''.join(tmpdata))
			except Exception, e:
				if self.log is not None:
					self.log.error('get data from %s Error:%s' % (self.__url, e))
				else:
					print 'get data from %s Error:%s' % (self.__url, e)
			finally:
				if res is not None:
					res.close()
			return data

	def __call():
		m = Method()
		return m.execute()

	return __call()
						
if __name__ == '__main__':
	print bind_api(
						path="pixiv_daily",
						date="20130828",
						dtype="json"
				)