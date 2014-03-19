#---------------------------------------------------------------------------------------------
#-
#- ModuleImporter.py
#- ---------------
#-
#- Module for managing servo (picam control)
#-
#- Author : Erwan Niquet
#- Date : Jan 2014
#- Part of raspadmin project, an Admin interface for raspberry pi
#-
#- Since RPIO seems incompatible with subprocess, all the part that manage GPIO is executed
#- throug subprocess command. Wait for improvement on the module RPIO to handle everything in
#- the script.
#--------------------------------------------------------------------------------------------

# -------------
# Import lib
# -------------


import time
import sys
import subprocess

# -------------
# Main class
# -------------

class ServoManager:
	_PWM_FREQUENCY = 50    # Hz
	_PWM_DMA_CHANNEL = 0
	_PWM_SUBCYLCLE_TIME_US = 1000/_PWM_FREQUENCY * 1000
	_PWM_PULSE_INCREMENT_US = 10
	_ZERO_US = 1500
	_MIN_US = _ZERO_US - 500	
	_MAX_US = _ZERO_US + 500
	_switchPinMode=False
	_switchPinNumber=-1
	_currentPulse=0

	def __init__(self,pinnum,minfreq=-1,maxfreq=-1,neutral=-1,inc=-1):
		if minfreq==-1: minfreq=self._MIN_US
		if maxfreq==-1: maxfreq=self._MAX_US
		if neutral==-1: neutral=self._ZERO_US
		if inc==-1: inc=self._PWM_PULSE_INCREMENT_US
		self._binaryPath= __file__	
		self._minFreq=minfreq
		self._maxFreq=maxfreq
		self._neutral=neutral
		self._inc=inc
		self._pinNumber=pinnum
		
	def setSwitchMode(self,pinnumber):
		self._switchPinMode=True
		self._switchPinNumber=pinnumber


	def setPulse(self,pulse):
		if self._switchPinMode:
			switch="1"
			switchpin=str(self._switchPinNumber)
		else:
			switch="0"
			switchpin="0"
	 	s = subprocess.check_output(["python",self._binaryPath,str(pulse),str(self._pinNumber),switch,switchpin])


	def start(self,initial=-1):
		if initial==-1: initial=self._neutral
		self._currentPulse=initial
		self.setPulse(self._currentPulse)
	
	def inc(self):
		self._currentPulse+=self._inc
		if self._inc>self._maxFreq:
			self._currentPulse=self._maxFreq
		self.setPulse(self._currentPulse)

	def dec(self):
		self._currentPulse-=self._inc
		if self._currentPulse<self._minFreq:
			self._currentPulse=self._minFreq
		self.setPulse(self._currentPulse)
# --------------------------------------------------------------------------
# The main function is executed by the script to handle RPIO call
# It is not very clean, but this is the only way I found in order to 
# manage the incompatibility of RPIO with subprocess (needed in other module)
# ---------------------------------------------------------------------------
		
	
def main():
	import RPIO
	import RPIO.PWM
	argv=sys.argv[1:]
	pulse=int(argv[0])
	pin=int(argv[1])
	switch=argv[2]
	switchpin=int(argv[3])
	RPIO.setmode(RPIO.BCM)		
	if switch=="1":
                RPIO.setup(switchpin, RPIO.OUT)
		RPIO.output(switchpin,True)
	
	servo = RPIO.PWM.Servo()
	servo.set_servo(pin, pulse)
	time.sleep(1)
	servo.stop_servo(pin)
	
	if switch=="1":
                RPIO.output(switchpin,False)
	RPIO.cleanup()
	

if __name__ == '__main__':
        main()
	

