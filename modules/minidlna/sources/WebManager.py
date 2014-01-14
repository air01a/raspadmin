from .. import WebStructure 
import minidlna
import json
from ..lib import FileManager
 
class WebManager(WebStructure.WebAbstract):
	def __init__(self,webconf):
		self.webconf=webconf
		self._dlna = minidlna.MiniDlna(webconf)
		self._filemanager=FileManager.FileManager('/')

        def browsedirectory(self,http_context):
                if 'base64_file' in http_context.http_get.keys():
                        path=self._filemanager.path_decode(http_context.http_get['base64_file'])
                else:
                        path='/'

                dirlist=self._filemanager.list_dir_from_path(path)
                return WebStructure.HttpContext(statuscode=200,content=json.dumps(dirlist),template=None,mimetype='text/html')


	def manage_action(self,http_context):
		post=http_context.http_post

                if 'alphanum_servicestatus' in post.keys():
                        ret=self._dlna.check_status()
			return (ret,'Service status')


                if 'alphanum_servicestart' in post.keys():
                        ret=self._dlna.start()
			return (ret,'Service start')

		if 'alphanum_servicestop' in post.keys():
                        ret=self._dlna.stop()
			return (ret,'Service stop')

		if 'alphanum_servicereload' in post.keys():
                        ret=self._dlna.reload()
			return (ret,'Service reload')

	def modify(self,post,status):
		path=post['base64_path']
		sharetype=post['alphanum_type']
		if sharetype not in ['music','photo','video','all']:
			return (1,'Type unknown')

		path=self._filemanager.path_decode(path)
		retcode=self._dlna.add_share(path,sharetype)
		if retcode==0:
			self._dlna.write_db()
			self._dlna.write_config()
			if status==0:
				self._dlna.reload()
		return (retcode,self._dlna.get_error(retcode))

	def get_html(self,http_context):

                if http_context.suburl=='browse':
                        return self.browsedirectory(http_context)

		template=['header.tpl','minidlna/minidlna.tpl','footer.tpl']
                sessionid=http_context.sessionid
                sessionvars=http_context.session.get_vars(sessionid)
		
		error=0
		errorstr="No Error"
		action=""

		post=http_context.http_post
                status=self._dlna.check_status()

		if http_context.suburl=='modify' and 'base64_path' in post.keys():
			(error,errorstr)=self.modify(post,status)

                if http_context.suburl=='delete' and 'base64_path' in post.keys():
                        error=self._dlna.delete_share(self._filemanager.path_decode(post['base64_path']),post['alphanum_type'])
			errorstr=self._dlna.get_error(error)
                        self._dlna.write_db()
                        self._dlna.write_config()
                        if status==0:
				self._dlna.reload()

			
		if 'alphanum_action' in post.keys():
			(retcode,service)=self.manage_action(http_context)
			if retcode==0:
				action=service+" : [OK]"
			else:
				error=retcode
				errorstr=service+" : [Failed]"

		shares=self._dlna.get_shares()
		return WebStructure.HttpContext(statuscode=200,content={'shares':shares,'status':status,'action':action,'error':error,'errorstr':errorstr,'token':sessionvars['posttoken']},template=template,mimetype='text/html')
		
        def get_module_name(self):
                return "Minidlna"

