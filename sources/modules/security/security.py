import re
import random
import string

class httpsecurity:
	_vartyperule={}

	def __init__(self):
		vartyperule={'str':'.*',
			     'date':'^[0-9]{2,4}[\/\-][0-9]{2}[\/\-][0-9]{2,4}$',
			     'alphanum':'^[0-9a-zA-Z _]*$',
                             'ldap':'^[a-zA-Z0-9]*$',
                             'email':'^[a-zA-Z0-9\-\_\.]*\@[a-zA-Z0-9\-\_]*\.[a-zA-Z]{2,3}$',
                             'id':'^[0-9]*$',
                             'num':'^-?[0-9]*$',
			     'base64':'^[A-Za-z0-9+/]*=?=?$'
			    }

		for vartype in vartyperule.keys():
			self._vartyperule[vartype]=re.compile(vartyperule[vartype])

	def geterror(self,num):
		error={0:'No Error',1:'No variable type',2:'Unknown type',3:'Variable does not respect security rules',5:'Post token not found',6:'Post Token not valid'}
		if num in error.keys():
			return error[num]
		return 'Unknown error'

	def checkhttpvars(self,httpvars):
		if httpvars==None:
			return 0
		for var in httpvars.keys():
			varsplit=var.split('_',1)
			if len(varsplit)!=2:
				return 1
			varname=varsplit[1]
			vartype=varsplit[0]
			if not vartype in self._vartyperule:
				return 2
			for item in httpvars[var]:
				if item!="" and not self._vartyperule[vartype].match(item):
					return 3
		return 0

	def checkposttoken(self,httpvars,sessionvars):
                if not 'alphanum_token' in httpvars.keys():
                	return 5

		if httpvars['alphanum_token']!=sessionvars['posttoken']:
			return 6
		return 0

	def generateposttoken(self):
		return ''.join(random.choice(string.ascii_letters+string.digits) for x in range(30))
