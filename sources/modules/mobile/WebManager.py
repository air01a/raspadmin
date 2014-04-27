from .. import WebStructure 
import io
import base64
import json
import ConfigParser

class WebManager(WebStructure.WebAbstract):
	def __init__(self,webconf):
		self.webconf=webconf

	def noError(self):
		return WebStructure.HttpContext(statuscode=200,content=json.dumps({'error':0,'errorstr':'No Error'}),template=None,mimetype='text/html')


	def get_html(self,http_context):
		sessionid=http_context.sessionid
		sessionvars=http_context.session.get_vars(sessionid)
                post=http_context.http_post

		content=http_context.module_manager.getmodulelist()
		return WebStructure.HttpContext(statuscode=200,content=json.dumps(content),template=None,mimetype='application/json')

        def get_module_name(self):
                return ""
