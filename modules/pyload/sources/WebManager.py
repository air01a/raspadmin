from .. import WebStructure 
import status
import pyload
import json

class WebManager(WebStructure.WebAbstract):
	def __init__(self,webconf):
		self.webconf=webconf
		self._pyload=pyload.PyLoad()
		self._pyload.connect()

	def manage_action(self,post):
		action=post['alphanum_action']
		if action == 'clearfinished':
			(error,status)=self._pyload.delete_finished_package()
			action='Finished package have been cleared'
			return (action,error,status)

		if action == 'addpackage' and 'alphanum_name' in post.keys() and 'str_links' in post.keys():
			links=post['str_links'].split("\n")
			name=post['alphanum_name']

			if len(name)==0 or len(links)==0:
				return ('',110,None)
			(error,status)=self._pyload.add_package(name,links) 
			action='Package added'
			return (action,error,status)

		if action == "startservice":
			error=self._pyload.start_process()
			action="Service Started"
			return (action,error,status)

		if action == "stopservice":
                        error=self._pyload.stop_process()
                        action="Service Stopped"
                        return (action,error,status)

		if action == "delete":
			if 'id_pid' not in post.keys():
				return ('',110,None)

			(error,status)=self._pyload.delete_package(post['id_pid'])
			action="Package deleted"
			return (action,error,status)

		if action == "refresh":
                        if 'id_pid' not in post.keys():
                                return ('',110,None)

                        (error,status)=self._pyload.restart_package(post['id_pid'])
                        action="Package reloaded"
                        return (action,error,status)

		if action == "restartfile":
			if 'id_fid' not in post.keys():
				return ('',110,None)
			(error,status)=self._pyload.restart_file(post['id_fid'])
			action="File restarted"
			return (action,error,status)

		if action == "deletefile":
			if 'id_fid' not in post.keys():
                                return ('',110,None)
			action="File Deleted"
			(error,status)=self._pyload.delete_file(post['id_fid'])
                        return (action,error,status)

		if action == "getcaptchatask":
	                (error,status)=self._pyload.getCaptcha()
			return ('Captcha',error,status)

		if action == "setcaptcha":
			if 'id_tid' not in post.keys() or 'str_captcha' not in post.keys():
				return ('',110,None)
			tid=post['id_tid']
			captcha=post['str_captcha'];
			(error,status)=self._pyload.setCaptcha(tid,captcha)
			return ('Set Captcha',error,status)

		return ('',0,None)

	def get_data(self,http_context):
		content={}
		if 'id_pid' in http_context.http_get.keys():
			print "ok"
			content=json.dumps(self._pyload.get_package_data(http_context.http_get['id_pid']))
		
		return WebStructure.HttpContext(statuscode=200,content=content,template=None,mimetype='text/html')

	def get_html(self,http_context):
		template=['header.tpl','pyload/pyload.tpl','footer.tpl']
                sessionid=http_context.sessionid
                sessionvars=http_context.session.get_vars(sessionid)

		error=0
		errorstr="No Error"
		action=""
		result=None

		if 'alphanum_action' in http_context.http_post.keys():
			(action,error,result)=self.manage_action(http_context.http_post)
			errorstr=self._pyload.get_error(error)

		if http_context.suburl=="getdata":
			return self.get_data(http_context)

		error1,download=self._pyload.get_current_download()
		error2,queue=self._pyload.get_queue()
		error3,status=self._pyload.get_status()

		if error1+error2+error3!=0:
			connected=False
		else:
			connected=True


		if http_context.suburl!="API":
			content={'connected':connected,'action':action,'error':error,'errorstr':errorstr,'status':status,'download':download,'queue':queue,'token':sessionvars['posttoken']}
		else:
			content=json.dumps({'action':action,'error':error,'errorstr':errorstr,'result':result})
			template=None

		return WebStructure.HttpContext(statuscode=200,content=content,template=template,mimetype='text/html')

        def get_module_name(self):
                return "PyLoad"

