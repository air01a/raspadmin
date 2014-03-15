import picamera

class PiCam:
	def __init__(self,width=600,height=480,rot=180):
		self._width=width
		self._height=height
		self._rot=rot
		self._active=False
		self._picam=None
		self._brightness=50
		self._exposureCompensation=0

	def start(self):
		if not self._active:
			self._picam=picamera.PiCamera()
			self._picam.rotation=self._rot
			self._active=True
			self.setBrightNess(self._brightness)
			self._picam.exposure_compensation=self._exposureCompensation


	def increaseBrightNess(self,value=10):
		self.setBrightNess(self._brightness+value)

	def decreaseBrightNess(self,value=10):
                self.setBrightNess(self._brightness-value)

        def increaseEvCp(self,value=5):
                self.setExposureCompensation(self._exposureCompensation+value)

        def decreaseEvCp(self,value=5):
                self.setExposureCompensation(self._exposureCompensation-value)



	def setBrightNess(self,value):
		if value<0:
			value=0
		if value>100:
			value=100 
		self._brightness=value
		if self._picam:
			self._picam.brightness=value

	def setExposureCompensation(self,value):
		if value<-25:
                        value=-25
		if value>25:
			value=25
		self._exposureCompensation=value
		if self._picam:
                        self._picam.exposure_compensation=value


	def stop(self):
		if self._active:
			self._picam.close()
			self._active=False

	def getPicture(self,output):
		if self._active:
			self._picam.capture(output=output, format='jpeg',resize=(self._width,self._height))

	def isActive(self):
		return self._active
