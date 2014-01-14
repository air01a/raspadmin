import RPi.GPIO as GPIO
import ConfigParser


class RaspGpio:
	_gpiostate={4:"N/A",GPIO.IN:"IN",GPIO.OUT:"OUT"}
	_comment={}
	IN=GPIO.IN
	OUT=GPIO.OUT
	HIGH=GPIO.HIGH
	LOW=GPIO.LOW	
	_init=False

	def __init__(self, configfile):
		GPIO.setwarnings(False)
		GPIO.setmode(GPIO.BCM)
		self.loadconf(configfile)
		
	def init(self):
		for pin in self._gpioavailable:
			self.setgpiomode(pin,GPIO.IN,True)
		self._init=True

	def isInitialized(self):
		return self._init

	def clean(self):
		self._init=False
		GPIO.cleanup()

	def loadconf(self,conf):
		config = ConfigParser.ConfigParser()
		config.readfp(open(conf))
		gpioavailable=config.get("GPIO", "portavailable").split(',')
		self._gpioavailable=[int(i) for i in gpioavailable]

		for pin in self._gpioavailable:
			option='gpio'+str(pin)+'comment'
			if config.has_option('GPIO',option):
				self._comment[pin]=config.get("GPIO", option)

	def setgpiomode(self,pin, mode, force=False):
		if not self._init and not force:
			return 10
		
		if not pin in self._gpioavailable:
			return 5

		if mode not in [GPIO.IN,GPIO.OUT]:
			return 7

		GPIO.setup(pin,mode)
		return 0

	def getgpiomode(self,pin,text=False):
                if not self._init:
                        return 10

                if not pin in self._gpioavailable:
                        return 5

		tmp=GPIO.gpio_function(pin)
		if text:
			return self._gpiostate[tmp]
		return tmp

	def readgpio(self,pin):
                if not self._init:
                        return 10

                if not pin in self._gpioavailable:
                        return 5

		return GPIO.input(pin)

	def setgpio(self,pin,value):

                if not self._init:
                        return 10

                if not pin in self._gpioavailable:
                        return 5
 

                if value not in [GPIO.HIGH,GPIO.LOW]:
                        return 6
                print "Set "+str(pin)+" to "+str(value)

		GPIO.output(pin,value)
		return 0

	def getavailablepin(self):
		return self._gpioavailable

	def getsummary(self):
                if not self._init:
                        return 10

		summary=[]
		for pin in self._gpioavailable:
			mode=self.getgpiomode(pin,True)
			read=self.readgpio(pin)
			if pin in self._comment.keys():
				comment=self._comment[pin]
			else:
				comment=''
			summary.append({'pin':pin,'mode':mode,'state':read,'comment':comment})
		return summary


	def geterrorstr(self,error):
		errorstr={0:'No error',5:'GPIO not available',6:'Incorrect State Value',7:'Incorrect Mode Value',10:'Module not initialized'}
		if error in errorstr.keys():
			return errorstr[error]
		return "Unknown error"		


#gpio=RaspGpio('/home/pi/raspadmin/conf/gpio.conf')
#print gpio.getsummary()

#for pin in gpio.getavailablepin():
#	print str(pin)+gpio.getgpiomode(pin,True)
#	try:
#		gpio.setgpiomode(pin,GPIO.OUT)
#	except:
#		print "oulala "+str(pin)

#GPIO.cleanup()
	
def main():
	gpio=RaspGpio('/home/pi/raspadmin/conf/gpio.conf')
	print gpio.getsummary()
	gpio.setgpiomode(17,GPIO.OUT)
	gpio.readgpio(17)
	print gpio.getsummary()

if __name__ == '__main__':
	main()
