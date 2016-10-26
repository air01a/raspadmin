from .. import WebStructure 
import json
import evohome

class WebManager(WebStructure.WebAbstract):
	def __init__(self,webconf):
		self.webconf=webconf
		self.evohome=evohome.EvoHome()

	def format_data(self,history):
		hours = history["base_hours"]
		abs="["
		for hour in history["base_hours"]:
			abs+=str(hour)+','
		abs=abs[:-1]+']'
		results={}
		for captor in history.keys():
			if captor!='base_hours':
				temp=""
				result=history[captor]
				for hour in hours:
					if hour in result.keys():
						temp+=str(result[hour])+','
					else:
						temp+='0,'
				temp='['+temp
				temp = temp[:-1]+']'
				results[captor]=temp
		results['abs']=abs
		return results
			
		
	def get_html(self,http_context):
		template=['header.tpl','evohome/evohome.tpl','footer.tpl']

                sessionid=http_context.sessionid
                sessionvars=http_context.session.get_vars(sessionid)
		
		(temperatures,weather)=self.evohome.getCurrentValues()
		history=self.format_data(self.evohome.getHistory())
		return WebStructure.HttpContext(statuscode=200,content={'token':sessionvars['posttoken'],'history':history,'weather':weather,'temperatures':temperatures},template=template,mimetype='text/html')
		

        def get_module_name(self):
                return "EvoHome"

