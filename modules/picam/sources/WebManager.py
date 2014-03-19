from .. import WebStructure 
from picam import PiCam
import io
import base64
import json
import ConfigParser
from servo import ServoManager

class WebManager(WebStructure.WebAbstract):
	def __init__(self,webconf):
		self.webconf=webconf
		self._picam = PiCam()
                config = ConfigParser.ConfigParser()
                config.readfp(open('/etc/raspadmin/picam.conf'))
		self._servoX=config.get("PICAM", "useServoXaxis")
		if self._servoX=="1":
			self._useGPIOPower       = config.get("PICAM", "useGpioPowerSwitch")
			self._servoPwNum         = int(config.get("PICAM","servoControlPinNumber"))
			self._maxServoPulse      = int(config.get("PICAM","maxServoPulse"))
			self._minServoPulse      = int(config.get("PICAM","minServoPulse"))
			self._defaultServoPulse  = int(config.get("PICAM","defaultServoPulse"))
			self._stepServoPulse     = int(config.get("PICAM","stepServoPulse"))
			self._servo = ServoManager(self._servoPwNum,self._minServoPulse, self._maxServoPulse, self._defaultServoPulse,self._stepServoPulse)
			if self._useGPIOPower == "1":
				self._switchGPIONum=int(config.get("PICAM", "switchPinNumber"))
				self._servo.setSwitchMode(self._switchGPIONum)
			
			self._servo.start()

	def get_image(self):
		my_stream = io.BytesIO()
		self._picam.getPicture(my_stream)
		return {'image':base64.b64encode(my_stream.getvalue())}

	def noError(self):
		return WebStructure.HttpContext(statuscode=200,content=json.dumps({'error':0,'errorstr':'No Error'}),template=None,mimetype='text/html')

	def webService(self,post):
		if not 'alphanum_action' in post.keys():
			return WebStructure.HttpContext(statuscode=200,content=None,template=None,mimetype='text/html')
		action=post['alphanum_action']

		if action=='light_inc':
			self._picam.increaseBrightNess()
			return self.noError()
		elif action=='light_dec':
			self._picam.decreaseBrightNess()
			return self.noError()
		elif action=='exposure_inc':
			self._picam.increaseEvCp()
			return self.noError()
		elif action=='exposure_dec':
                        self._picam.decreaseEvCp()
			return self.noError()
		elif action=='movex_inc' and self._servoX=="1":
			self._servo.inc()
			return self.noError()
		elif action=='movex_dec' and self._servoX=="1":
			self._servo.dec()
			return self.noError()

		return WebStructure.HttpContext(statuscode=200,content=None,template=None,mimetype='text/html')


	def get_html(self,http_context):
		template=['header.tpl','picam/picam.tpl','footer.tpl']
		sessionid=http_context.sessionid
		sessionvars=http_context.session.get_vars(sessionid)
                post=http_context.http_post

		if http_context.suburl=='getimage' and self._picam.isActive():
			content=json.dumps(self.get_image())
			return WebStructure.HttpContext(statuscode=200,content=content,template=None,mimetype='text/html')
		elif http_context.suburl=='ws':
			return self.webService(post)
		elif http_context.suburl=='start':
			self._picam.start()
		elif http_context.suburl=='stop':
			self._picam.stop()	
		content={'isActive':self._picam.isActive(),'token':sessionvars['posttoken'],'manageServoX':self._servoX,'gpioSwitch':self._useGPIOPower}	
		return WebStructure.HttpContext(statuscode=200,content=content,template=template,mimetype='text/html')

        def get_module_name(self):
                return "PiCam"
