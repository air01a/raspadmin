from .. import WebStructure 
from gpio import RaspGpio
import json
import time

class WebManager(WebStructure.WebAbstract):
	def __init__(self,webconf):
		self.webconf=webconf
                self._gpio=RaspGpio(webconf['confdir']+'/gpio.conf')

	def set_mode(self,pin,mode):
		if mode=='IN':
			mode=self._gpio.IN
		else:
			mode=self._gpio.OUT
		error=self._gpio.setgpiomode(int(pin),mode)
		content={'summary':self._gpio.getsummary()}
		content['error']=error
                content['errormsg']=self._gpio.geterrorstr(error)

		content=json.dumps(content)
		return WebStructure.HttpContext(statuscode=200,content=content,template=None,mimetype='text/html')


	def set_state(self, pin, state):
		print state
		error=self._gpio.setgpio(int(pin),int(state))
                content={'summary':self._gpio.getsummary()}
                content['error']=error
                content['errormsg']=self._gpio.geterrorstr(error)

                content=json.dumps(content)

                return WebStructure.HttpContext(statuscode=200,content=content,template=None,mimetype='text/html')


	def get_html(self,http_context):
		template=['header.tpl','gpio/gpio.tpl','footer.tpl']

                sessionid=http_context.sessionid
                sessionvars=http_context.session.get_vars(sessionid)
		
		if (http_context.suburl=='init' and not self._gpio.isInitialized()):
			self._gpio.init()
		
                if (http_context.suburl=='clean'):
                        self._gpio.clean()

		if self._gpio.isInitialized():
			if (http_context.suburl=='mode'):
				return self.set_mode(http_context.http_post['num_pin'],http_context.http_post['alphanum_mode'])
				
			if (http_context.suburl=='state'):
				return self.set_state(http_context.http_post['num_pin'],http_context.http_post['alphanum_state'])

			summary=self._gpio.getsummary()
		
		else:
			summary=None
				
		return WebStructure.HttpContext(statuscode=200,content={'summary':summary,'token':sessionvars['posttoken']},template=template,mimetype='text/html')
		

        def get_module_name(self):
                return "Gpio"

