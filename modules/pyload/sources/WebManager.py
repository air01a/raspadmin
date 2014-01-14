from .. import WebStructure 
import status
import pyload

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
			return (action,error)

		if action == 'addpackage' and 'alphanum_name' in post.keys() and 'str_links' in post.keys():
			links=post['str_links'].split("\n")
			name=post['alphanum_name']

			if len(name)==0 or len(links)==0:
				return ('',110)
			(error,status)=self._pyload.add_package(name,links) 
			action='Package added'
			return (action,error)

		if action == "startservice":
			error=self._pyload.start_process()
			action="Service Started"
			return (action,error)

		if action == "stopservice":
                        error=self._pyload.stop_process()
                        action="Service Stopped"
                        return (action,error)

		if action == "delete":
			if 'id_pid' not in post.keys():
				return ('',110)

			(error,status)=self._pyload.delete_package(post['id_pid'])
			action="Package deleted"
			return (action,error)

		if action == "refresh":
                        if 'id_pid' not in post.keys():
                                return ('',110)

                        (error,status)=self._pyload.restart_package(post['id_pid'])
                        action="Package deleted"
                        return (action,error)

		return ('',0)

	def get_html(self,http_context):
		template=['header.tpl','pyload/pyload.tpl','footer.tpl']
                sessionid=http_context.sessionid
                sessionvars=http_context.session.get_vars(sessionid)

		error=0
		errorstr="No Error"
		action=""

		if 'alphanum_action' in http_context.http_post.keys():
			(action,error)=self.manage_action(http_context.http_post)
			errorstr=self._pyload.get_error(error)

		error1,download=self._pyload.get_current_download()
		error2,queue=self._pyload.get_queue()
		error3,status=self._pyload.get_status()

		if error1+error2+error3!=0:
			connected=False
		else:
			connected=True
		content={'connected':connected,'action':action,'error':error,'errorstr':errorstr,'status':status,'download':download,'queue':queue,'token':sessionvars['posttoken']}

		return WebStructure.HttpContext(statuscode=200,content=content,template=template,mimetype='text/html')

        def get_module_name(self):
                return "PyLoad"

