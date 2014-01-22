import ConfigParser
from xmlrpclib import ServerProxy
from base64 import standard_b64encode
from ..lib import process


class NzbGet:
        def __init__(self):
                config = ConfigParser.ConfigParser()
                config.readfp(open('/etc/raspadmin/nzbget.conf'))
                self._url=config.get("NZBGET", "url")
                self._user=config.get("NZBGET", "user")
                self._password=config.get("NZBGET", "password")
		self._protocol=config.get("NZBGET", "protocol")
		self._server=ServerProxy(self._protocol+"://"+self._user+":"+self._password+"@"+self._url)
		self._start=config.get("NZBGET", "start").split(' ')
		self._stop=config.get("NZBGET", "stop").split(' ')
		self._tmpfiles=config.get("NZBGET", "tmpdir")

	def get_tmp(self):
		return self._tmpfiles

        def get_format_size(self,number):
                extension = [ 'b', 'Kb', 'Mb','Gb' ]
                for i in range(len(extension)):
                        if number/1024<1:
                                return str(round(number,2))+ " " + extension[i]
                        else:
                                number=number/1024+0.0
		return str(round(number*1024,2))+" "+"Gb"


	def get_status(self):
		try:
			result=self._server.status()
		except:
			return (1,None)
		result['DownloadRateFormated']=self.get_format_size(result['DownloadRate'])
		result['RemainingSizeLoFormated']=self.get_format_size(result['RemainingSizeLo'])
		result['DownloadedSizeLoFormated']=self.get_format_size(result['DownloadedSizeMB']*1024*1024)
		#| bug with DownloadedSizeLo that does not show the correct value???
		result['AverageDownloadRateFormated']=self.get_format_size(result['AverageDownloadRate'])
		return (0,result)


	def get_url_queue(self):
                try:
			result=self._server.urlqueue()
		except:
			return (1,None)

		return (0,result)

	def get_list_groups(self):
		try:
			result=self._server.listgroups()
                except:
                        return (1,None)

		for i in range(len(result)):
			result[i]['RemainingSizeLoFormated']=self.get_format_size(result[i]['RemainingSizeLo'])
			result[i]['FileSizeLoFormated']=self.get_format_size(result[i]['FileSizeLo'])
			result[i]['DownloadedFormated']=self.get_format_size(result[i]['FileSizeLo']-result[i]['RemainingSizeLo'])
		return (0,result)

	def get_history(self):
                try:
			result=self._server.history()
                except:
                        return (1,None)

		for i in range(min(len(result),10)):
			result[i]['FileSizeLoFormated']=self.get_format_size(result[i]['FileSizeLo'])
			if result[i]['UnpackStatus']=="SUCCESS":
				status="Success"
			else:
				if result[i]['DeleteStatus']!='None':
					status="Deleted"
				else:
					status="Failed"
			result[i]['status']=status	
		
		if len(result)>10:
			result=result[0:10]
		return (0,result)


	def get_post_queue(self):
		try:
			result=self._server.postqueue(10)
		except:
			return (1,None)

		for i in range(len(result)):
			result[i]['StageProgress']=int(result[i]['StageProgress']/10)
			
		return (0,result)


	def add_nzb(self,filename,category,addtotop):
		try:
			in_file = open(filename, "r")
			nzbcontent = in_file.read()
			in_file.close()
			nzbcontent64=standard_b64encode(nzbcontent)
			self._server.append(filename,category,addtotop,nzbcontent64)
		except:
			return (1,None)
		return (0,None)

	def delete_package(self,id):
		try:
			result=self._server.editqueue('GroupDelete',0,'',[int(id)])
		except:
			return (1,None)

		if result:
			return 0
		
		return 11

	def get_error_str(self,error):	
		errorstr={0:'No Error',1:'Connexion to nzbget api failed',11:'Deletion failed'}
		if error in errorstr.keys():
			return errorstr[error]
		return 'Unknown error'

	def start_process(self):
                return process.execute(self._start)

        def stop_process(self):
                return process.execute(self._stop)

		

def main():
	nzbget=NzbGet()
	print nzbget.get_status()
#{'PostJobCount': 0, 'ServerPaused': False, 'ThreadCount': 10, 'UrlCount': 0, 'RemainingSizeHi': 0, 'FreeDiskSpaceLo': 4294967295L, 'UpTimeSec': 123, 'DownloadRate': 1995308, 'FreeDiskSpaceHi': 4294967295L, 'FreeDiskSpaceMB': 0, 'ResumeTime': 0, 'ScanPaused': False, 'Download2Paused': False, 'AverageDownloadRate': 1896387, 'DownloadedSizeHi': 0, 'RemainingSizeLo': 2733540781L, 'DownloadPaused': False, 'ServerTime': 1390219826, 'DownloadLimit': 0, 'DownloadTimeSec': 123, 'ServerStandBy': False, 'DownloadedSizeMB': 222, 'FeedActive': False, 'PostPaused': False, 'DownloadedSizeLo': 233255617, 'NewsServers': [{'Active': True, 'ID': 1}], 'RemainingSizeMB': 2606, 'ParJobCount': 0}

	print nzbget.get_url_queue()
	print nzbget.get_list_groups()
#[{'NZBName': 'lost-brave.720p.sample.mkv', 'Category': '', 'DeleteStatus': 'NONE', 'Parameters': [{'Name': '*Unpack:', 'Value': 'yes'}], 'MoveStatus': 'NONE', 'RemainingSizeLo': 2787260897L, 'UnpackStatus': 'NONE', 'MaxPriority': 0, 'MinPostTime': 1351869402, 'RemainingSizeHi': 0, 'Health': 1000, 'LastID': 71, 'PausedSizeMB': 289, 'FileCount': 71, 'FileSizeMB': 3116, 'Deleted': False, 'SuccessArticles': 572, 'DupeKey': '', 'MaxPostTime': 1351869460, 'MarkStatus': 'NONE', 'NZBID': 1, 'ScriptStatuses': [], 'FailedArticles': 0, 'ActiveDownloads': 4, 'MinPriority': 0, 'DestDir': '/root/downloads/inter/lost-brave.720p.sample.mkv.#1', 'FileSizeLo': 3267834963L, 'FirstID': 4, 'NZBFilename': 'lost-brave.720p.sample.mkv.nzb', 'DupeScore': 0, 'FinalDir': '', 'FileSizeHi': 0, 'ScriptStatus': 'NONE', 'RemainingSizeMB': 2658, 'ServerStats': [{'ServerID': 1, 'FailedArticles': 0, 'SuccessArticles': 620}], 'PausedSizeHi': 0, 'TotalArticles': 4185, 'NZBNicename': 'lost-brave.720p.sample.mkv', 'PausedSizeLo': 303705281, 'RemainingFileCount': 59, 'RemainingParCount': 9, 'DupeMode': 444076, 'ParStatus': 'NONE', 'CriticalHealth': 897}]
	print nzbget.get_history()

	#nzbget.add_nzb('/tmp/test.nzb','',False)

if __name__ == '__main__':
        main()

