from .. import WebStructure 
import ConfigParser
from downloader import DownloadManager
import json
import rarfile
from threading import Thread

class WebManager(WebStructure.WebAbstract):
	def __init__(self,webconf):
		self.webconf=webconf
		config = ConfigParser.ConfigParser()
                config.readfp(open('/etc/raspadmin/downloader.conf'))
		self.path=config.get("PATH","downloadrep")
		self.downloadManager = DownloadManager(self.path)
		rarfile.UNRAR_TOOL = "unrar-nonfree"

	def manage_download(self,str_list):
		list_download = [y for y in (x.strip() for x in str_list.splitlines()) if y]
		for url in list_download:
			self.downloadManager.addDownload(url)

	def unrar(self,file):
		if self.downloadManager.updateStatus(file,'r'):
			try:
				o=rarfile.RarFile(self.path+'/'+file)
				o.extractall(self.path)
				self.downloadManager.updateStatus(file,'dr')
			except Exception as e:
				self.downloadManager.updateStatus(file,'df')

	def get_html(self,http_context):
		template=['header.tpl','downloader/downloader.tpl','footer.tpl']
		sessionid=http_context.sessionid
		sessionvars=http_context.session.get_vars(sessionid)
                post=http_context.http_post

		if 'str_download' in post.keys():
			self.manage_download(post['str_download'])

		if http_context.suburl=='getInfo' :
			return WebStructure.HttpContext(statuscode=200,content=json.dumps(self.downloadManager.downloadStatus()), template=None, mimetype='text/html')
		if http_context.suburl=='unrar' and 'str_file' in http_context.http_get:
			try:
				t = Thread(target=self.unrar, args = (http_context.http_get['str_file'],))
   				t.daemon = True
    				t.start()
			except Exception as e:
				print repr(e)
				

		content={'token':sessionvars['posttoken'],'includefile':'downloader/headerdownloader.html'}	
		return WebStructure.HttpContext(statuscode=200,content=content,template=template,mimetype='text/html')

        def get_module_name(self):
                return "Downloader"
