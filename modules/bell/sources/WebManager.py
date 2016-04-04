from .. import WebStructure 
import json
import time
import os
class WebManager(WebStructure.WebAbstract):
	def __init__(self,webconf):
		self.webconf=webconf

	def get_html(self,http_context):
		template=['header.tpl','bell/bell.tpl','footer.tpl']

                sessionid=http_context.sessionid
                sessionvars=http_context.session.get_vars(sessionid)
		
		if http_context.suburl=="ACK":
			if os.path.isfile("/tmp/BELLRESPONSE"):
				os.remove("/tmp/BELLRESPONSE")

		if os.path.isfile("/tmp/BELLRESPONSE"):
			isFile=True
		else:
			isFile=False

				
		return WebStructure.HttpContext(statuscode=200,content={'isFile':isFile,'token':sessionvars['posttoken']},template=template,mimetype='text/html')
		

        def get_module_name(self):
                return "Bell"

