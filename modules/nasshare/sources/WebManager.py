from .. import WebStructure 
from ..lib import FileManager
from SambaManager import SambaManager
import json
 
class WebManager(WebStructure.WebAbstract):
	def __init__(self,webconf):
		self.webconf=webconf
		self._sambamanager=SambaManager(webconf)
		self._filemanager=FileManager.FileManager(self._sambamanager.get_base_dir())

	def browsedirectory(self,http_context):
                if 'base64_file' in http_context.http_get.keys():
                        path=self._filemanager.path_decode(http_context.http_get['base64_file'])
                else:
                        path='/'

		dirlist=self._filemanager.list_dir_from_path(path)
		return WebStructure.HttpContext(statuscode=200,content=json.dumps(dirlist),template=None,mimetype='text/html')

	def modify(self,http_context):
		template=['header.tpl','share/modify.tpl','footer.tpl']
                sessionid=http_context.sessionid
                sessionvars=http_context.session.get_vars(sessionid)
	
		post=http_context.http_post
		path=post['base64_path']
		pathtxt=self._filemanager.path_decode(path)
		error=0
		errorstr='No error'
		
		
		if 'alphanum_action' in post.keys():
			name=post['alphanum_name']
			comment=post['str_comment']
			public=True if 'alphanum_public' in post.keys() else False
			writable=True if 'alphanum_writable' in post.keys() else False
			readonly=True if 'alphanum_readonly' in post.keys() else False
			reader=post['str_reader']
			writer=post['str_writer']
			if len(reader)>1 and reader[-1]==',':
				reader=reader[:-1]
			if len(writer)>1 and writer[-1]==',':
				writer=writer[:-1]
			error=self._sambamanager.modify_share(name,pathtxt,comment,readonly,public,writable,writer,reader,True)
			if error==0:
				self._sambamanager.write_samba_config()
				return None
			errorstr=self._sambamanager.get_error(error)
			share={}
			share['name']=name
			share['comment']=comment
			share['readonly']=readonly
			share['public']=public
			share['writable']=writable
			share['validusers']=reader
			share['writelist']=writer		
		else:	
			share=self._sambamanager.find_share_from_path(pathtxt)


		if share!=None:
			name=share['name']
			comment=share['comment']
			readonly="checked" if share['readonly'] else ""
			public="checked" if share['public'] else ""
			writable="checked" if share['writable'] else ""
			writelist=[i for i in share['writelist'].split(',') if i in self._sambamanager.get_nas_user()]
			validusers=[i for i in share['validusers'].split(',') if i in self._sambamanager.get_nas_user()]
			alluserreadtmp=self._sambamanager.get_nas_user()
			alluserwritetmp=self._sambamanager.get_nas_user()
			alluserread=[i for i in alluserreadtmp if not i in validusers]
			alluserwrite=[i for i in alluserwritetmp if not i in writelist]

		else:
                        name=""
			comment=""
                        readonly=""
                        public=""
                        writable=""
                        writelist=[]
                        validusers=[]
			alluserread=self._sambamanager.get_nas_user()
                        alluserwrite=self._sambamanager.get_nas_user()
			action="new"

		content={'path':path,'pathtxt':pathtxt,'token':sessionvars['posttoken'],'name':name,'comment':comment,'readonly':readonly,'public':public,'writable':writable,'writelist':writelist,'validusers':validusers,'alluserread':alluserread,'alluserwrite':alluserwrite}

		return WebStructure.HttpContext(statuscode=200,content=content,template=template,mimetype='text/html')


	def get_html(self,http_context):
		template=['header.tpl','share/share.tpl','footer.tpl']
                sessionid=http_context.sessionid
                sessionvars=http_context.session.get_vars(sessionid)
		
		error=0
		errorstr="No Error"
		action=""

		if http_context.suburl=='browse':
			return self.browsedirectory(http_context)

		if http_context.suburl=='delete':
			if 'base64_path' in http_context.http_post.keys():
				path=http_context.http_post['base64_path']
		                pathtxt=self._filemanager.path_decode(path)
				share=self._sambamanager.find_share_from_path(pathtxt)
				if share:
					self._sambamanager.delete_share(share['name'])
					action="Share %s has been deleted"%(share['name'])


		if http_context.suburl=='modify':
			if 'base64_path' in http_context.http_post.keys():
				ret=self.modify(http_context)
				if ret!=None:
					return ret
				action="Share modified"
		self._sambamanager.clean_db()
		share=self._sambamanager.get_db()
		

		return WebStructure.HttpContext(statuscode=200,content={'share':share,'action':action,'error':error,'errorstr':errorstr,'token':sessionvars['posttoken']},template=template,mimetype='text/html')
		

        def get_module_name(self):
                return "NAS-Share"

