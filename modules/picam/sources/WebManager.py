from .. import WebStructure 
import io
import base64
import json
import ConfigParser
from servo import ServoManager
import picamera

class WebManager(WebStructure.WebAbstract):
	def __init__(self,webconf):
		self.webconf=webconf
		self.isActive = False
		self.camera = None
		self._brightness=50
		self._exposureCompensation=0

                config = ConfigParser.ConfigParser()
                config.readfp(open('/etc/raspadmin/picam.conf'))
		self._servoX=config.get("PICAM", "useServoXaxis")

		self._useGPIOPower       = config.get("PICAM", "useGpioPowerSwitch")
		if self._servoX=="1":
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

	def stream(self,http):

		self.camera = picamera.PiCamera()
		self.camera.resolution = (640,480)
		self.camera.framerate=15
		self.camera.rotation=180
		http.send_response(200)
		http.send_header('Content-type', 'multipart/x-mixed-replace; boundary=--jpgboundary')
		http.end_headers()
		my_stream = io.BytesIO()
		try:
			for frameR in self.camera.capture_continuous(my_stream, format="jpeg", use_video_port=True):
				my_stream.truncate()
				my_stream.seek(0)
				http.wfile.write("--jpgboundary\r\n".encode())
				http.end_headers()
				http.wfile.write(my_stream.getvalue())
		except:
			self.camera.close()
			self.camera = None

	def noError(self):
		return WebStructure.HttpContext(statuscode=200,content=json.dumps({'error':0,'errorstr':'No Error'}),template=None,mimetype='text/html')


	def setBrightNess(self,value):
		value += self._brightness
		if value<0:
			value=0
		if value>100:
			value=100 
		self._brightness=value
		if self.camera:
			self.camera.brightness=value

	def setExposureCompensation(self,value):
		value += self._exposureCompensation
		if value<-25:
			value=-25
		if value>25:
			value=25
		self._exposureCompensation=value
		if self.camera:
			self.camera.exposure_compensation=value

	def webService(self,post):
		if not 'alphanum_action' in post.keys():
			return WebStructure.HttpContext(statuscode=200,content=None,template=None,mimetype='text/html')
		action=post['alphanum_action']

		if action=='light_inc':
			self.setBrightNess(10)
			return self.noError()
		elif action=='light_dec':
			self.setBrightNess(-10)
			return self.noError()
		elif action=='exposure_inc':
			self.setExposureCompensation(10)
			return self.noError()
		elif action=='exposure_dec':
                        self.setExposureCompensation(-10)
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


		if http_context.suburl=='getimage.mjpg':
			self.stream(http_context.directhttp)

		if http_context.suburl=='getimage' and self._picam.isActive():
			content=json.dumps(self.get_image())
			return WebStructure.HttpContext(statuscode=200,content=content,template=None,mimetype='text/html')
		elif http_context.suburl=='ws':
			return self.webService(post)
		elif http_context.suburl=='start':
			self.isActive=True
		elif http_context.suburl=='stop':
			self.isActive=False	
		content={'isActive':self.isActive,'token':sessionvars['posttoken'],'manageServoX':self._servoX,'gpioSwitch':self._useGPIOPower}	
		return WebStructure.HttpContext(statuscode=200,content=content,template=template,mimetype='text/html')

        def get_module_name(self):
                return "PiCam"
