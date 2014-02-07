import json
import requests

from ..lib import process
import ConfigParser


class PyLoad:
	def __init__(self):
                config = ConfigParser.ConfigParser()
                config.readfp(open('/etc/raspadmin/pyload.conf'))
		self._baseurl=config.get("PYLOAD", "baseurl")
		self._login=config.get("PYLOAD", "login")
		self._password=config.get("PYLOAD", "password")
		self._start=config.get("PYLOAD", "start").split(' ')
		self._stop=config.get("PYLOAD","stop").split(' ')
		self._connected=False
		self._session=''
	
	def _send_request(self,request,vars):
		try:
			rs = requests.post(request,data=vars)
			return rs
		except:
			return None

	def send_request(self,request,vars={}):
		vars['session']=self._session

		result=self._send_request(request,vars)

		if result!=None and result.status_code==403:
			self.connect()
			result=self._send_request(request,vars)

		return result

	def connect(self):
		vars={"username":self._login,"password":self._password}
		result=self._send_request(self._baseurl+"login",vars)
	
		if result==None:
			return 12
	
		if result.status_code!=200:
			return 11

		self._session=json.loads(result.text)
		if self._session==False:
			return 10

		self._connected=True
		
		return 0

	def get_api(self,api,vars={}):
		result=self.send_request(self._baseurl+api,vars)
		if result==None:
			return (11,0)

		if result.status_code!=200:
                        return (11,str(result.status_code))
		return (0,json.loads(result.text))

	def get_current_download(self):
		(error,result)=self.get_api('statusDownloads')
		if error!=0:
                        return (error,result)

		for i in range(len(result)):
                        result[i]['format_speed'] = self.get_format_size(result[i]['speed'])
                return (0,result)


	def get_format_size(self,number):
		extension = [ 'b', 'Kb', 'Mb','Gb' ]
		for i in range(len(extension)):
			if number/1024<1:
				return str(int(number))+ " " + extension[i]
			else:
				number=number/1024
	
	def get_queue(self):
		(error,result) = self.get_api('getQueue')
		if error!=0:
			return (error,result)

		for i in range(len(result)):
			result[i]['sizetotalformated'] = self.get_format_size(result[i]['sizetotal'])
			result[i]['sizedoneformated'] = self.get_format_size(result[i]['sizedone'])
		return (0,result)


	def get_status(self):
		return self.get_api('statusServer')

	def get_package_data(self,pid):
		vars={'pid':pid}
		return self.get_api('getPackageData',vars)

	def delete_finished_package(self):
		return self.get_api('deleteFinished')

	def delete_package(self,pid):
		vars={'pids':json.dumps([pid])}
		return self.get_api('deletePackages',vars)

	def restart_file(self,fid):
		vars={'fid':fid}
		return self.get_api('restartFile',vars)


	def getCaptcha(self):
		vars={}
		if not self.get_api('isCaptchaWaiting',vars):
			return False

		return self.get_api('getCaptchaTask',vars)

	def setCaptcha(self,tid,value):
		vars={'tid':json.dumps(tid),'result':json.dumps(value)}
		return self.get_api('setCaptchaResult',vars);

	def delete_file(self,fid):
		vars={'fids':json.dumps([fid])}
		return self.get_api('deleteFiles',vars)

	def restart_package(self,pid):
		vars={'pid':pid}
		return self.get_api('restartPackage',vars)

	def add_package(self,name,links,password=None):
		vars={'name':json.dumps(name)}
		vars['links']=json.dumps(links)
		return self.get_api('addPackage',vars)

	def get_error(self,error):
		errorstr={0:'No Error',10:'Login to pyload failed',11:'Error while communicating with pyload', 110:'Values can not be empty'}
		if error in errorstr.keys():
			return errorstr[error]
		return 'Unknown error'

	def start_process(self):
		return process.execute(self._start)

	def stop_process(self):
		return process.execute(self._stop)

def main():
	pyload=PyLoad()

if __name__ == '__main__':
	main()

