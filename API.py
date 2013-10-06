
from bindAPI import bind_api
from bindAPI import openurl
from Pixiv import Pixiv
import lxml.etree as etree
import urllib2
import utils
from StringIO import StringIO

class API(object):

	host = 'http://www.pixiv.net'
	def __init__(self, path='', log = None):
		self.path = path
		self.log = log

	daily = bind_api(
						path="/ranking.php",
						mode="daily",
						allow_parameters =['p', 'date']
				)

	weekly = bind_api(
						path="/ranking.php",
						mode="weekly",
						allow_parameters =['p', 'date']
				)

	male = bind_api(
						path="/ranking.php",
						mode="male",
						allow_parameters =['p', 'date']
				)

	female = bind_api(
						path="/ranking.php",
						mode="female",
						allow_parameters =['p', 'date']
				)

	male_r18 = bind_api(
						path="/ranking.php",
						mode="male_r18",
						allow_parameters =['p', 'date']
				)

	female_r18 = bind_api(
						path="/ranking.php",
						mode="female_r18",
						allow_parameters =['p', 'date']
				)

	monthly = bind_api(
						path="/ranking.php",
						mode="monthly",
						allow_parameters =['p', 'date']
				)

	rookie = bind_api(
						path="/ranking.php",
						mode="rookie",
						allow_parameters =['p', 'date']
				)

	original = bind_api(
						path="/ranking.php",
						mode="original",
						allow_parameters =['p', 'date']
				)

	def download_picture(self, url, illust_id):
		# 'src': 'http://i2.pixiv.net/img08/img/blade4649/38902616.jpg'
		referer = "%s/member_illust.php?mode=big&illust_id=%s" % (self.host, illust_id)
		name = url.split('?')[0].split('/')[-1]
		with open(self.path+name, 'wb') as f:
			f.write(self.get_picture_stream(url, illust_id))

	def get_picture_stream(self, url, illust_id, ungzip=True):
		referer = "%s/member_illust.php?mode=big&illust_id=%s" % (self.host, illust_id)
		request = urllib2.Request(						
				url=url,
				headers={
								'Accept-Encoding':	'gzip, deflate',
								'Accept':	'image/png,image/*;q=0.8,*/*;q=0.5',
								'Referer':	referer,
								})
		response = urllib2.urlopen(request)
		if not ungzip:
			tmp_stream = utils.ungzip(response)
		else:
			tmp_stream = StringIO(response.read()).getvalue()
		response.close()
		return tmp_stream

def main():
	p = Pixiv('mulvren@126.com', '11908298')
	p.login()
	api = API()
	api.download_picture('http://i1.pixiv.net/img-inf/img/2013/10/05/00/03/21/38915840_s.jpg', '38915840')

if __name__ == '__main__':
	main()
			