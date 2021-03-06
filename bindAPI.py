#!/usr/bin/python
#-*-coding:utf8-*-

import time
import urllib2
import urllib
import Pixiv
import lxml.html as html
import datetime
import utils

def bind_api(**config):

	class Method(object):

		path = config['path']
		mode = config.get('mode', 'daily')
		use_gzip = config.get('use_gzip', True)
		allow_parameters = config.get('allow_parameters', [])
		# data = config.get('data', datetime.datetime.now().strftime("%Y%m%d"))
		host = config.get('host', 'http://www.pixiv.net')

		def __init__(self, args, kargs):
			self.paramters = dict()
			for k, v in kargs.items():
				if v is None:
					continue
				if k in self.allow_parameters:
					try:
						self.paramters[k] = utils.convert_to_utf8_str(v)
					except Exception, e:
						raise "parse paramters errors: " + e

			self.paramters['mode'] = utils.convert_to_utf8_str(self.mode)
			self.__url = "%s?%s" % (self.host + self.path, urllib.urlencode(self.paramters))
			self.log = Pixiv.logger

		def __medium_member_illust(self, url):
				self.log.info("open url: %s" % url)
				doc = openurl(url, Pixiv.timeout, self.use_gzip)
				rated_count = doc.cssselect('dd.rated-count')[0].text
				caption = doc.cssselect('p.caption')[0].text
				tags = []
				for t in doc.cssselect('li.tag'):
					tags.append(t.cssselect('a.text')[0].text)
				mode = doc.cssselect('div.works_display')[0].iter('a').next().attrib['href']
				src = doc.cssselect('div.works_display')[0].iter('img').next().attrib['src']
				#TODO add comment
				return rated_count, caption, tags, src, utils.parse_url_params(mode.split('?')[1])['mode']

		def __big_mode(self, illust_id):
			url = "%s/member_illust.php?mode=big&illust_id=%s" % (self.host, illust_id)
			referer = "%s/member_illust.php?mode=medium&illust_id=%s" % (self.host, illust_id)
			doc = openurl(url, Pixiv.timeout, self.use_gzip,
									headers={'Referer':	referer})
			src = doc.xpath('/html/body/img')[0].attrib['src']
			return src

		def __manga_mode(self, illust_id):
			url = "%s/member_illust.php?mode=manga&illust_id=%s" % (self.host, illust_id)
			referer = "%s/member_illust.php?mode=medium&illust_id=%s" % (self.host, illust_id)
			doc = openurl(url, Pixiv.timeout, self.use_gzip,
									headers={'Referer':	referer})
			src = [ x.attrib['data-src'] for x in doc.cssselect('img.image')]
			return src

		def __big_member_illust(self, illust_id, mode='big'):
			if mode == 'big' :
				return self.__big_mode(illust_id)
			elif mode == 'manga' :
				return self.__manga_mode(illust_id)


		def execute(self):
			self.log.info("open url: %s" % self.__url)
			doc = openurl(self.__url, Pixiv.timeout, self.use_gzip)
			result = []
			for el in doc.cssselect('div.ranking-item'):
				eldata = dict()
				src = dict()
				eldata['src'] = src
				eldata['rank'] = el.attrib['id']
				#user
				user = el.cssselect('a.user-container')[0]
				user_id = utils.parse_url_params(user.attrib['href'].split('?')[1])['id']
				user_icon = user.getchildren()[0].attrib['data-src']
				user_name = user.getchildren()[1].text
				dictuser = {'id': user_id, 'icon': user_icon, 'name': user_name}
				eldata['user'] = dictuser

				src['small'] = el.cssselect('img._thumbnail')[0].attrib['src']

				etitle = el.cssselect('a.title')[0]
				eldata['title'] = etitle.text
				#EXAMPLE member_illust.php?mode=medium&illust_id=38892600&ref=rn-b-1-title&uarea=male_r18
				href = etitle.attrib['href']
				eldata['illust_id'] = utils.parse_url_params(href.split('?')[1])['illust_id']

				data = el.cssselect('dl.inline-list')[0]
				eldata['views_count'] = data.getchildren()[1].text
				eldata['score_count'] = data.getchildren()[3].text
				
				eldata['date'] = el.cssselect('dl.inline-list')[1].getchildren()[1].text

				eldata['rated_count'], eldata['caption'], eldata['tags'], src['medium'], mode = self.__medium_member_illust(self.host + "/" + href)
				src['big'] = self.__big_member_illust(eldata['illust_id'], mode)
				result.append(eldata)
			return result


	def __call(*args, **kargs):
		m = Method(args, kargs)
		return m.execute()

	return __call

def openurl(url, timeout, use_gzip=True, headers={}):
		doc = None
		try:
			request = urllib2.Request(
														url=url,
														headers=headers)
			if use_gzip:
				request.add_header('Accept-encoding', 'gzip')
			connection = urllib2.urlopen(request, timeout=timeout)
			doc = html.document_fromstring(utils.ungzip(connection))
			connection.close()
			return doc
		except Exception, e:
			raise "open url: %s error(%s): %s" % (url, e.errno, e.strerror)
						
if __name__ == '__main__':
	# /ranking.php
	p = Pixiv.Pixiv('youraccout', 'yourpwd')
	print p.login()
	c = bind_api(
						path="/ranking.php",
						mode="male",
						allow_parameters =['p']
				)
	print c(p='1')