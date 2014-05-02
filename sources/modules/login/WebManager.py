from .. import WebStructure 
from ..HttpAlert import httpalert
import os
import pam
import json

class WebManager(WebStructure.WebAbstract):
	def __init__(self,webconf):
		self._webconf=webconf

	def get_html(self,http_context):
		no_auth=['.jpg','.png','.css','.ico','.htm']
		
		if http_context.module=='static' and (http_context.url[-4:] in no_auth):
			return None

		sessionid=http_context.sessionid
		if 'num_logout' in http_context.http_get.keys():
			http_context.session.del_var(sessionid,'CONNECTED')

		error=''
		connected=False
		sessionvars=http_context.session.get_vars(sessionid)

		if 'CONNECTED' in sessionvars.keys():	
			if not 'alphanum_json' in http_context.http_get.keys():
				return None
			else:
				connected=True
                                error='No Error'

		http_post=http_context.http_post
		http_post_varlist=http_post.keys()
		allowedlogin=self._webconf['login_allowusers'].split(',')
		loginmodule=self._webconf['login_pammodule']
		if 'alphanum_login' in http_post_varlist and 'str_password' in http_post_varlist:
			if http_post['alphanum_login'] in allowedlogin and pam.authenticate(http_post['alphanum_login'],http_post['str_password'], loginmodule):
				http_context.session.add_var(sessionid,'CONNECTED',True)
				http_context.session.add_var(sessionid,'user',http_post['alphanum_login'])

				if not 'alphanum_json' in http_context.http_get.keys():
					return None
				connected=True
				error='No Error'
			else:
				error='Wrong credentials'
		token=sessionvars['posttoken']
	
		content={'page':http_context.url,'error':error,'token':token,'connected':connected}
		if 'alphanum_json' in http_context.http_get.keys():
			template=None
			content=json.dumps(content)
			http_context.session.add_var(sessionid,'API',True)
		else:
			template='login.tpl'

		return WebStructure.HttpContext(statuscode=200,content=content,template=template,mimetype='text/html')

	def is_required(self):
		return True
