from .. import WebStructure 
import json
import time
import os
import psutil
import ConfigParser
from subprocess import call
from time import sleep

class WebManager(WebStructure.WebAbstract):
	def __init__(self,webconf):
		self.webconf=webconf
		config = ConfigParser.ConfigParser()
		config.readfp(open('/etc/raspadmin/bell.conf'))
		self._port=int(config.get("NET", "port"))
		self._start="/usr/sbin/service bell start"
		self._stop="/usr/sbin/service bell stop"

	def get_html(self,http_context):
		template=['header.tpl','bell/bell.tpl','footer.tpl']

                sessionid=http_context.sessionid
                sessionvars=http_context.session.get_vars(sessionid)
		
		if http_context.suburl=="ACK":
			if os.path.isfile("/tmp/BELLRESPONSE"):
				os.remove("/tmp/BELLRESPONSE")
		
		if http_context.suburl=="RLD":
			call(['/usr/sbin/service','bell','start'])	
			sleep(0.5)
		if http_context.suburl=="STP":
			call(['/usr/sbin/service','bell','stop'])
			sleep(0.5)

		if http_context.suburl=="TEST":
			call(['/usr/bin/python','/opt/bell/send.py'])
			sleep(1)
		
		if os.path.isfile("/tmp/BELLRESPONSE"):
			isFile=True
		else:
			isFile=False

		isOpen=False
		for conn in psutil.net_connections():
			if conn.laddr[1]==self._port and conn.type==2:
				isOpen=True

				
		return WebStructure.HttpContext(statuscode=200,content={'isOpen':isOpen,'isFile':isFile,'token':sessionvars['posttoken']},template=template,mimetype='text/html')
		

        def get_module_name(self):
                return "Bell"

