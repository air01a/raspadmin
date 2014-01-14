from .. import WebStructure 
from ..HttpAlert import httpalert
import os
import pam

class WebManager(WebStructure.WebAbstract):
	def __init__(self,webconf):
		self._webconf=webconf

	def get_html(self,http_context):
		no_auth=['.jpg','.png','.css','.ico']
		
		if http_context.module=='static' and (http_context.url[-4:] in no_auth):
			return None

		sessionid=http_context.sessionid
		if 'num_logout' in http_context.http_get.keys():
			http_context.session.del_var(sessionid,'CONNECTED')

		error=''
		sessionvars=http_context.session.get_vars(sessionid)

		if 'CONNECTED' in sessionvars.keys():	
			return None

		http_post=http_context.http_post
		http_post_varlist=http_post.keys()
		allowedlogin=self._webconf['login_allowusers'].split(',')
		loginmodule=self._webconf['login_pammodule']
		if 'alphanum_login' in http_post_varlist and 'str_password' in http_post_varlist:
			if http_post['alphanum_login'] in allowedlogin and pam.authenticate(http_post['alphanum_login'],http_post['str_password'], loginmodule):
				http_context.session.add_var(sessionid,'CONNECTED',True)
				http_context.session.add_var(sessionid,'user',http_post['alphanum_login'])
				return None
			else:
				error='Wrong credentials'
		token=sessionvars['posttoken']
		return WebStructure.HttpContext(statuscode=200,content={'page':http_context.url,'error':error,'token':token},template='login.tpl',mimetype='text/html')

	def is_required(self):
		return True
