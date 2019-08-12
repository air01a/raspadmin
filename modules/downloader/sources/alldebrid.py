import requests
import json

class AllDebrid:
	def __init__(self, token,agent):
		self._getProvider()
		self._token=token
		self._agent=agent
		self.headers = {
                        	'User-Agent': 'raspadmin_v1'
                	}

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


	def getLink(self,url):
		req = requests.get("https://api.alldebrid.com/link/unlock?agent=%s&token=%s&link=%s" % (self._agent,self._token,url),headers=self.headers)
		data = json.loads(req.content)

		if "error" in data.keys():
			if data["errorCode"]!=0:
				print(data)
				print(data["errorCode"])
			return (data["error"],"")
		else:
			return (0,data["infos"]["link"])

