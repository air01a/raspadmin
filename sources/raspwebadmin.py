#---------------------------------------------------------------------------------------------
#-
#- raspwebadmin.py
#- ---------------
#-
#- Webserver for raspadmin
#- 
#- Author : Erwan Niquet
#- Date : Jan 2014
#- Part of raspadmin project, an Admin interface for raspberry pi
#- 
#--------------------------------------------------------------------------------------------

# -------------
# Import lib
# -------------

# Base lib
import sys
from os import curdir, sep, path
import time
import traceback
# Http lib
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from SocketServer     import ThreadingMixIn
import Cookie
import urlparse
import cgi
import ssl
#html lib
from quik import FileLoader
#custom lib
import configreader
from modules.WebStructure import HttpContext
from modules.ModuleImporter import ModuleImporter
import modules.HttpAlert
from modules.HttpAlert import httpalert
from modules.SessionManager import SessionManager
# ----------------------------
# Custom HTTP request handler
# ----------------------------
class HttpRequestHandler(BaseHTTPRequestHandler):
    # Vars
    _debug = False # Set it to True if you want to debug
    # Override default value for server header
    server_version = 'raspadmin v1.0'
    sys_version = '- Python let you guess -'

    # Print a debug message
    def debug(self,message,complement=None):
	if self._debug==True:
		print message,
		if complement:
			print complement,
		print ""

    # Get GET variables
    def gethttpvar(self,path):
	http_get={}

	split_url = urlparse.urlsplit(path)
	http_get = urlparse.parse_qs(split_url[3])
	for i in http_get.keys():
		http_get[i]=http_get[i][0]

	cookies=None
	if "Cookie" in self.headers:
		cookies={}
		cookiesobj = Cookie.SimpleCookie(self.headers["Cookie"])
		for cookiename,morsel in cookiesobj.iteritems():
			cookies[morsel.key]=morsel.value
	return (split_url[2], http_get,cookies)

    # Send HTTP response
    def renderer(self,title,http_response,extraheaders):
	self.send_response(http_response.statuscode)
	self.send_header('Content-type',http_response.mimetype)

        if hasattr(http_response,'lastmodified'):
                self.send_header('Last-Modified',self.date_time_string(http_response.lastmodified))
        else:
                self.send_header('Last-Modified',self.date_time_string(time.time()))


	if hasattr(http_response,'headers'):
		for header in http_response.headers.keys():
			self.send_header(header,http_response.headers[header])
	
	for header in extraheaders:
		headertab=header.split(':',1)
		self.send_header(headertab[0],headertab[1])

	self.end_headers()

	if http_response.template==None:
		if not http_response.hasVar('outputfile' ):
			self.wfile.write(http_response.content)
		else:
			try:
				f = open(http_response.outputfile, "rb")
				byte = f.read(4*1024*1024)
				while byte != "":
					self.wfile.write(byte)
					byte = f.read(4*1024*1024)
			except:
				pass
	else:
		if not 'includefile' in http_response.content.keys():
			http_response.content['includefile']='None'

		http_response.content['menulist']=moduleManager.getmodulelist()	
		http_response.content['pagetitle']=title
		if not isinstance( http_response.template, (list, tuple)):
			http_response.template=[http_response.template]
		for temp in http_response.template:
			template = tplloader.load_template(temp)
			self.wfile.write(template.render(http_response.content,loader=tplloader).encode('utf-8'))

    # Security check
    def security(self,url,http_get,http_post,http_cookies):
        self.debug("Entering Security :",url)

	self.router(url,http_get,http_post,http_cookies)

    def internalerror(self,error):
 	if self._debug:
        	error+=traceback.format_exc()
        print error
        self.send_response(500)
	self.end_headers()
	template = tplloader.load_template('500.tpl')
        self.wfile.write(template.render({'error':error},loader=tplloader).encode('utf-8'))

    # Send the request to the correct module
    # in the URL, the module is defined by the first directory
    # Example GET /static/404.html will send the request to the static modules (if defined)
    # The static module has to manage this request, and send back a object with the response
    def router(self,url,http_get,http_post,http_cookies):
	# Normalisez path
	url=path.normpath(url)
	self.debug("Entering router ",url)	
	(ipclient,portclient)=self.client_address

	# Analyse the URL to find the module
	urlanalyzer=url.split('/')
	if len(urlanalyzer)<2 or urlanalyzer==['','']:
		module='status'
		suburl=url
	else:
		module=urlanalyzer[1]
		if (moduleManager.moduleexists(module)):
			if len(urlanalyzer)>2:
				suburl=url.split('/',2)[2]
			else:
				suburl='/index'
		else:
			module='static'
			suburl=url

	# Manage session
	extraheaders=[]
	sessionid=sessionmanager.get_id(http_cookies)
	if not sessionid:
		sessionid,cookie=sessionmanager.create(configreader.webconf['usessl'])
		extraheaders.append(cookie)
	
	# Create the http context to send to the module
        http_context=HttpContext(http_get=http_get,http_post=http_post,url=url,suburl=suburl,ipclient=ipclient, cookies=http_cookies, sessionid=sessionid, session=sessionmanager, module=module,servername=self.headers.get('Host'))

	# Check if there is required module to go through
	for requiredmodule in moduleManager.getrequiredmodules():
		try:
			http_response=requiredmodule.get_html(http_context)
		except Exception, e:
                	self.internalerror("Erreur while handling mandatory modules\n")
			return

		if http_response!=None:
		        self.renderer('',http_response,extraheaders) # if required module does not return None, the module has priority to all others
			return
	# If no required modules has return something, let's continue		
	
	# Send the module
	http_response=moduleManager.getmodule(module).get_html(http_context)

	# Pass the response to the renderer function
	try:
		http_response=moduleManager.getmodule(module).get_html(http_context)
	except Exception, e:
                self.internalerror(error="Erreur while handling the requested module\n")
		return
	self.renderer(moduleManager.getmodule(module).get_module_name(),http_response,extraheaders)


    # Manage Get response
    def do_GET(self):
	(path,http_get,http_cookies) = self.gethttpvar(self.path)
	self.security(path,http_get,{},http_cookies)

    # Manage Post response
    def do_POST(self):
	http_post={}
	try:
	
		(path,http_get,http_cookies) = self.gethttpvar(self.path)
		form = cgi.FieldStorage(
        	    fp=self.rfile,
            	    headers=self.headers,
            	    environ={'REQUEST_METHOD': 'POST',
                    'CONTENT_TYPE': self.headers['Content-Type']})
		if form:
			for field in form.keys():
				if form[field].file:
					http_post[field]=form[field].file		
				else:
					http_post[field]=form[field].value
	except Exception, e:
		self.internalerror("Erreur while handling your post request\n")
		return

	self.security(path,http_get,http_post,http_cookies)

    
# ----------------------------
# Threaded HttpServer
# ----------------------------

# This class is only present for adding multithreadig capabilites to the HTTP server
class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    pass

# ----------------------------
# Main
# ----------------------------
def main():
    moduleManager.loadmodulelist('WebManager',configreader.globalconf)

    try:
        server = ThreadedHTTPServer(('', int(configreader.webconf['httpport'])), HttpRequestHandler)
	if (configreader.webconf['usessl']=='yes'):
		# If ssl is activated, wrap the socket with SSL layer
		server.socket = ssl.wrap_socket (server.socket, keyfile=configreader.webconf['keyfile'], certfile=configreader.webconf['certfile'],server_side=True)
        print 'started httpserver...'
        server.serve_forever()
    except KeyboardInterrupt:
        print '^C received, shutting down server'
        server.socket.close()

# -------------------------------------
# Create global objects and run main()
# -------------------------------------
if __name__ == '__main__':
    # Create global objects that will be shared with all thread
    moduleManager=ModuleImporter(configreader.moduleconf)
    tplloader=FileLoader(configreader.webconf['templatesdir'])
    sessionmanager=SessionManager()
    main()
