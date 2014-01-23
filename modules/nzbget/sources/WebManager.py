from .. import WebStructure 
import status
import json
import nzbget
import os

class WebManager(WebStructure.WebAbstract):
	def __init__(self,webconf):
		self.webconf=webconf
		self._nzbget=nzbget.NzbGet()

	def manage_action(self,post,sessionid,sessionvars):

		action=post['alphanum_action']

		if action=="startservice":
			error=self._nzbget.start_process()
			if error!=0:
				return (error,'')
			return (error,'Service starting, please refresh')
		
		elif action=="stopservice":
			error=self._nzbget.stop_process()
                        if error!=0:
                                return (error,'')
                        return (error,'Service is stopping, please refresh')

	
	def forge_filename(self,filename):
		auth="ABCDEFGHIJKLLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_-. "
		ret=""
		for i in filename:
			if i in auth:
				if i==" ":
					ret+="_"
				else:
					ret+=i
		return ret

	def add_download(self,post,sessionid,sessionvars):
		if 'str_name' not in post.keys() or 'file_nzbd' not in post.keys() or 'filename_nzbd' not in post.keys():
			return (0,'')
		if post['str_name']!='':
			filename=self.forge_filename(post['str_name'])
		else:
		        filename=post['filename_nzbd']

		if 'alphanum_addtotop' in post.keys():
			addtotop=True
		else:
			addtotop=False
                try:
			f = open(self._nzbget.get_tmp()+"/"+filename, "wb")
                        byte = post['file_nzbd'].read(4*1024*1024)
                        while byte != "":
                        	f.write(byte)
                                byte = post['file_nzbd'].read(4*1024*1024)
			f.close()
			post['file_nzbd'].close()
                except:
			print "oups"
                	return (10,'')
		ret=self._nzbget.add_nzb(self._nzbget.get_tmp()+"/"+filename,'',addtotop)
		os.remove(self._nzbget.get_tmp()+"/"+filename)
		
		return (ret,'Download added')


	def delete_package(self,post):
		if 'id_id' not in post.keys():
			return (0,'')

		return (self._nzbget.delete_package(post['id_id']),'package deleted')


	def get_html(self,http_context):
		template=['header.tpl','nzbget/nzbget.tpl','footer.tpl']
                sessionid=http_context.sessionid
                sessionvars=http_context.session.get_vars(sessionid)

		post=http_context.http_post
		content={}
		error=0
		errorstr="No Error"
		action=""

		if 'alphanum_action' in post.keys():
			(error,action)=self.manage_action(post,sessionid,sessionvars)
		
		if http_context.suburl=='adddownload':
			(error,action)=self.add_download(post,sessionid,sessionvars)

		if http_context.suburl=='deletepackage':
			(error,action)=self.delete_package(post)

		(error1,status)=self._nzbget.get_status()
		if error1==0:
			(error1,listgroups)=self._nzbget.get_list_groups()
			(error2,postqueue)=self._nzbget.get_post_queue()
			(error3,history)=self._nzbget.get_history()
		else:
			listgroups=[]
			postqueue=[]
			history=[]
		if error==0:
			error=error1
		else:
			if action!="":
				error=0
		errorstr=self._nzbget.get_error_str(error)
		token=sessionvars['posttoken']
		content={'token':token,'status':status,'listgroups':listgroups,'error':error,'errorstr':errorstr,'action':action,'postqueue':postqueue,'history':history}
		return WebStructure.HttpContext(statuscode=200,content=content,template=template,mimetype='text/html')

        def get_module_name(self):
                return "NZBGet"

