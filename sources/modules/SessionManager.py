import Cookie
import random
import string

class SessionManager:
	_session={}

	def get_id(self,http_cookies):
		if http_cookies==None:
			return None
		if not 'RASPSESSION' in http_cookies.keys():
			return None

		sessionid=http_cookies['RASPSESSION']

		if not sessionid in self._session.keys():
			return None

		return sessionid

	def get_vars(self,sessionid):
		if not sessionid in self._session.keys():
                        return None
		
		return  self._session[sessionid]

	def create(self, SSL):
		sessionid=''.join(random.choice(string.ascii_letters+string.digits) for x in range(30))
		C = Cookie.SimpleCookie()
		C['RASPSESSION']=sessionid
		C['RASPSESSION']["path"] = "/"
		C['RASPSESSION']['expires'] = 24 * 60 * 60
		C['RASPSESSION']['secure'] = '1'
		if SSL=='yes':
			C['RASPSESSION']['secure'] = '1'
		C['RASPSESSION']['httponly']='1'
		self._session[sessionid]={}
		return sessionid,C.output()

	def add_var(self,sessionid,name,value):
		self._session[sessionid][name]=value

	def del_var(self,sessionid,name):
		if name in  self._session[sessionid].keys():
			del self._session[sessionid][name]
			
		

#sess=SessionManager()
#sessionid,cookie=sess.create()
#print cookie

#sess.add_var(sessionid,'test',1)
#print sess.get_vars(sessionid)
#sess.del_var(sessionid,'test')
#print sess.get_vars(sessionid)
		
