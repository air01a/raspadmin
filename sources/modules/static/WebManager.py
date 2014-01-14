from .. import WebStructure 
import mimetypes
import os

class WebManager(WebStructure.WebAbstract):
	_mime={'js':'application/x-javascript','css':'text/css'}

	def __init__(self,webconf):
		self.webconf=webconf

	def get_html(self,http_context):
		if http_context.suburl=='/':
			http_context.suburl='/index.html'

		file=self.webconf['staticfiledir']+'/'+http_context.suburl
		try:
			f = open(file)
			statbuf = os.stat(file)
			content=f.read()
			f.close()
			statuscode=200
			
			ext=http_context.suburl.split('.')[-1]
#			if ext in self._mime.keys():
#				mimetype=self._mime[ext]
#			else:
			mimetype=mimetypes.guess_type(file)[0]

			return WebStructure.HttpContext(statuscode=statuscode,content=content,template=None,mimetype=mimetype,lastmodified=statbuf.st_mtime)
		except IOError,e:
			if e.errno==2:
				return WebStructure.HttpContext(statuscode=404,content={'page':http_context.url},template='404.tpl',mimetype='text/html')
			return WebStructure.HttpContext(statuscode=503,content={'page':http_context.url},template='503.tpl',mimetype='text/html')

	def get_html_header(self,http_context):
		return ""

	def get_module_name(self):
		return ""
