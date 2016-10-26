from .. import WebStructure 
import ConfigParser
from downloader import DownloadManager
import json

class WebManager(WebStructure.WebAbstract):
	def __init__(self,webconf):
		self.webconf=webconf
		config = ConfigParser.ConfigParser()
                config.readfp(open('/etc/raspadmin/downloader.conf'))
		self.path=config.get("PATH","downloadrep")
		self.downloadManager = DownloadManager(self.path)

	def manage_download(self,str_list):
		list_download = [y for y in (x.strip() for x in str_list.splitlines()) if y]
		for url in list_download:
			self.downloadManager.addDownload(url)

	def get_html(self,http_context):
		template=['header.tpl','downloader/downloader.tpl','footer.tpl']
		sessionid=http_context.sessionid
		sessionvars=http_context.session.get_vars(sessionid)
                post=http_context.http_post

		if 'str_download' in post.keys():
			self.manage_download(post['str_download'])

		if http_context.suburl=='getInfo' :
			return WebStructure.HttpContext(statuscode=200,content=json.dumps(self.downloadManager.downloadStatus()), template=None, mimetype='text/html')

		content={'token':sessionvars['posttoken'],'includefile':'downloader/headerdownloader.html'}	
		return WebStructure.HttpContext(statuscode=200,content=content,template=template,mimetype='text/html')

        def get_module_name(self):
                return "Downloader"
