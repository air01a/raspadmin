from .. import WebStructure 
from ..HttpAlert import httpalert
import mimetypes
import os
import security

class WebManager(WebStructure.WebAbstract):
	def __init__(self,webconf):
		self._webconf=webconf
		self._security=security.httpsecurity()

	def get_html(self,http_context):
		if not 'posttoken' in http_context.session.get_vars(http_context.sessionid):
			http_context.session.add_var(http_context.sessionid,'posttoken',self._security.generateposttoken())


		if http_context.module=='static':
			return None

	        securitycheck=self._security.checkhttpvars(http_context.http_get)
	        if securitycheck!=0:
        	        return httpalert(self._security.geterror(securitycheck))

                securitycheck=self._security.checkhttpvars(http_context.http_post)
                if securitycheck!=0:
                        return httpalert(self._security.geterror(securitycheck))

		if http_context.http_post!={}:
			securitycheck=self._security.checkposttoken(http_context.http_post,http_context.session.get_vars(http_context.sessionid))
			if securitycheck!=0:
				return httpalert(self._security.geterror(securitycheck))
		
		return None


	def is_required(self):
		return True

	def priority(self):
		return True 
