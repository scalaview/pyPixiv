from StringIO import StringIO
import gzip

def parse_url_params(url):
	data = {}
	for params in url.split('&'):
		el = params.split('=')
		if el is not None and len(el)>1:
			data[el[0]] = el[1]

	return data


def convert_to_utf8_str(arg):
		# written by Michael Norton (http://docondev.blogspot.com/)
		if isinstance(arg, unicode):
		    arg = arg.encode('utf-8')
		elif not isinstance(arg, str):
		    arg = str(arg)
		return arg


def ungzip(response):

		if response.info().get('Content-Encoding') == 'gzip':
			buf = StringIO(response.read())
			f = gzip.GzipFile(fileobj=buf)
			data = f.read()
		else:
			data = response.read()
		return data

		