#---------------------------------------------------------------------------------------------
#-
#- SessionManager.py
#- ---------------
#-
#- Manage the user session for raspadmin
#-
#- Author : Erwan Niquet
#- Date : Jan 2014
#- Part of raspadmin project, an Admin interface for raspberry pi
#-
#--------------------------------------------------------------------------------------------

# -------------
# Import lib
# -------------
import Cookie
import random
import string
import time
# -------------
# Main object
# -------------
class SessionManager:
	_session={}

	# Get the id (in the list) of the session with the cookie
	def get_id(self,http_cookies):
		if http_cookies==None:
			return None

		if not 'RASPSESSION' in http_cookies.keys():
			return None


		sessionid=http_cookies['RASPSESSION']

		if not sessionid in self._session.keys():
			return None

		if self._session[sessionid]['expiration']<time.time():
			del self._session[sessionid]
			print "# Warning : used of expired cookie"
			return None

		return sessionid

	# return all variables stored for the session id
	def get_vars(self,sessionid):
		if not sessionid in self._session.keys():
                        return None
		
		return  self._session[sessionid]

	# Create a session, and return a cookie
	def create(self, SSL):
		sessionid=''.join(random.choice(string.ascii_letters+string.digits) for x in range(30))
		C = Cookie.SimpleCookie()
		C['RASPSESSION']=sessionid
		C['RASPSESSION']["path"] = "/"
		C['RASPSESSION']['expires'] = 86400
		C['RASPSESSION']['secure'] = '1'
		if SSL=='yes':
			C['RASPSESSION']['secure'] = '1'
		C['RASPSESSION']['httponly']='1'
		self._session[sessionid]={'expiration':time.time()+ 86400}
		return sessionid,C.output()

	# Add a variable to session
	def add_var(self,sessionid,name,value):
		self._session[sessionid][name]=value

	# Del var from session
	def del_var(self,sessionid,name):
		if name in  self._session[sessionid].keys():
			del self._session[sessionid][name]
