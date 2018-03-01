import requests
import json

class AllDebrid:
	def __init__(self, login, password):
		self.login = login
		self.password = password
		self._getProvider()		
		self._authenticate()

	def _getProvider(self):
             	try:
			req = requests.get("https://api.alldebrid.com/hosts")
                        #self._provider = [ x.lstrip()[1:-1] for x in req.content.split(',') ]
			data = json.loads(req.content)

			self._provider = [ x["domain"] for x in data["hosts"] ]
			for x in data["hosts"]:
				if "altDomains" in x.keys():
					self._provider+=x["altDomains"]
                except:	
			self._provider= []

	def isProvider(self, url):
		for p in self._provider:
			if url.find(p)!=-1:
				return True

		return False

	def _authenticate(self):
		url = "https://api.alldebrid.com/user/login?username=%s&password=%s" % (self.login,self.password)
		req = requests.get(url)
		data = json.loads(req.content)
		if 'success' in data.keys():
			self._token = data['token']
			return 0
		else:
			self._token=None
			return 1
	
	def getLink(self,url):
		req = requests.get("https://api.alldebrid.com/link/unlock?token=%s&link=%s" % (self._token,url))
		data = json.loads(req.content)
		
		if "error" in data.keys():
			if data["errorCode"]==1:
				self._authenticate()
				return self.getLink(url)
			return (data["error"],"")
		else:
			return (0,data["infos"]["link"])
		
