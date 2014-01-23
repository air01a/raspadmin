from .. import WebStructure 
import status
import pyload
import json
from ..lib import FileManager
import ConfigParser
import os
import mimetypes

class WebManager(WebStructure.WebAbstract):
	def __init__(self,webconf):
		config = ConfigParser.ConfigParser()
                config.readfp(open('/etc/raspadmin/filemanager.conf'))
                self._basedir=config.get("FILEMANAGER", "basedir")
		self._filemanager=FileManager.FileManager(self._basedir)
		self._function={'listdir':{'ptr':self.list_dir,'args':['base64_dir']},
				'createdir':{'ptr':self.create_dir,'args':['base64_path','filename_dir']},
				'delete':{'ptr':self.delete_file,'args':['base64_path']},
				'copy':{'ptr':self.copy_file,'args':['base64_src','base64_dst']},
				'move':{'ptr':self.move_file,'args':['base64_src','base64_dst']}
				}


	def _return(self,content,error=0,errorstr='No Error'):
		data={'error':error,'errorstr':errorstr,'data':content}
		return  WebStructure.HttpContext(statuscode=200,content=json.dumps(data),template=None,mimetype='text/html')

	def copy_file(self,post):
		return self.move_file(post,True)

	def move_file(self,post,copy=False):
                src=self._filemanager.path_decode(post['base64_src'])
		dst=self._filemanager.path_decode(post['base64_dst'])
		if copy:
			action="Copy"
		else:
			action="Move"

		if not self._filemanager.validate_path(src) or not self._filemanager.validate_path(dst):
			return self._return({'action':action,'src':src,'dst':dst},1001,'Invalid path')
		
		if copy:
			if os.path.isdir(src):
				dst+='/'+os.path.basename(src)
				error=self._filemanager.dir_copy(src,dst)
			else:
				error=self._filemanager.file_copy(src,dst)
		else:
			error=self._filemanager.file_move(src,dst)

		return self._return({'src':src,'dst':dst,'action':action},error,self._filemanager.get_error(error))
			

	def delete_file(self,post):
		path=self._filemanager.path_decode(post['base64_path'])
		if not self._filemanager.validate_path(path):
                        return self._return({},1001,'Invalid path')
		if os.path.isdir(path):
			error=self._filemanager.rm_tree(path)
		else:
			error=self._filemanager.rm_file(path)
		return self._return({},error,self._filemanager.get_error(error))

	def create_dir(self,post):
		path=self._filemanager.path_decode(post['base64_path'])
		if not self._filemanager.validate_path(path):
			return self._return({},1001,'Invalid path')

		newdir=path+'/'+post['filename_dir']
		error=self._filemanager.make_dir(newdir)
		return self._return({},error,self._filemanager.get_error(error))

	def list_dir(self,post):
		path=self._filemanager.path_decode(post['base64_dir'])

		directory=self._filemanager.list_dir_from_path(path)
		files=self._filemanager.list_file_from_path(path)

		completefile=[]
		for f in directory:
			tmp={}
			tmp['name']=f['pathname']
			tmp['link']=f['link']
			tmp['type']='dir'
			tmp['size']=''
			completefile.append(tmp)

		for f in files:
			tmp={}
			tmp['name']=f['pathname']
                        tmp['link']=f['link']
                        tmp['type']='file'
                        tmp['size']=f['size']
			completefile.append(tmp)

		return self._return(completefile)

	def file_download(self,path):
		file=self._filemanager.path_decode(path)
		if self._filemanager.validate_path(file):
	                try:
	                        statbuf = os.stat(file)
        	                statuscode=200
                        	mimetype=mimetypes.guess_type(file)[0]
				header={'Content-Disposition':'attachment; filename="'+os.path.basename(file)+'"'};
                        	return WebStructure.HttpContext(headers=header,outputfile=file,statuscode=statuscode,content=None,template=None,mimetype=mimetype,lastmodified=statbuf.st_mtime)
	                except OSError,e:
        	                return WebStructure.HttpContext(statuscode=404,content={'page':http_context.url},template='404.tpl',mimetype='text/html')
                	else:
				pass
		return WebStructure.HttpContext(statuscode=503,content={'page':http_context.url},template='503.tpl',mimetype='text/html')


	def get_html(self,http_context):
		template=['header.tpl','filemanager/filemanager.tpl','footer.tpl']
                sessionid=http_context.sessionid
                sessionvars=http_context.session.get_vars(sessionid)
		post=http_context.http_post
		get=http_context.http_get

		error=0
		errorstr="No Error"
		action=""

		if http_context.suburl=='download' and 'base64_file' in get.keys():
			return self.file_download(get['base64_file'])

		if 'alphanum_action' in post.keys():
			action=post['alphanum_action']
			if action in self._function.keys():
				func=self._function[action]
				ptr=func['ptr']
				args=func['args']
				for item in args:
					if item not in post.keys():
						return self._return(None,1001,'Missing argument')
				return ptr(post)
				


		content={'includefile':'filemanager/headerfilemanager.html','token':sessionvars['posttoken']}


		return WebStructure.HttpContext(statuscode=200,content=content,template=template,mimetype='text/html')

        def get_module_name(self):
                return "FileManager"

