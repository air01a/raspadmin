from .. import WebStructure 
from ManageUserNas import ManageUser

 
class WebManager(WebStructure.WebAbstract):
	def __init__(self,webconf):
		self.webconf=webconf
		self._manageuser=ManageUser(webconf)

	def modifyuser(self,http_context):
		post=http_context.http_post

		print post.keys()
		if 'alphanum_action' not in post.keys():
			return (0,"No error","")
		
		action=post['alphanum_action']
		if action=='add':
			if 'alphanum_user' not in post.keys() or 'str_password' not in post.keys():
				return (3,"Missing parameters","")
			if 'str_comment' not in post.keys():
				post['str_comment']='No information'
			error=self._manageuser.createUser(post['alphanum_user'],post['str_comment'],post['str_password'])
			return (error,self._manageuser.get_error(error),"User %s has been added"%post['alphanum_user'])
		elif action=='delete':
			if 'alphanum_name' not in post.keys():
				return (3,"Missing parameters","")
			error=self._manageuser.del_user(post['alphanum_name'])
			return (error,self._manageuser.get_error(error),"User %s has been deleted"%post['alphanum_name'])
		elif action=='change':
			if 'alphanum_name' not in post.keys() or 'str_password' not in post.keys():
                                return (3,"Missing parameters","")
	
			error=self._manageuser.set_password(post['alphanum_name'], post['str_password'])
			return (error,self._manageuser.get_error(error),"Password for user %s has been changed" % post['alphanum_name'])

		else:
			return (2,"Unknown action","")

	def get_html(self,http_context):
		template=['header.tpl','user/user.tpl','footer.tpl']
                sessionid=http_context.sessionid
                sessionvars=http_context.session.get_vars(sessionid)
		
		error=0
		errorstr="No Error"
		action=""

		if (http_context.suburl=="manageuser" and http_context.http_post!={}):
			(error,errorstr,action)=self.modifyuser(http_context)

		users=self._manageuser.get_nas_user()
		return WebStructure.HttpContext(statuscode=200,content={'action':action,'error':error,'errorstr':errorstr,'users':users,'token':sessionvars['posttoken']},template=template,mimetype='text/html')
		

        def get_module_name(self):
                return "NAS-User"

