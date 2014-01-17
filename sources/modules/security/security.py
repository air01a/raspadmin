#---------------------------------------------------------------------------------------------
#-
#- security.py
#- ---------------
#-
#- Security check with token (csrf protection) and variable type (injection)
#-
#- Author : Erwan Niquet
#- Date : Jan 2014
#- Part of raspadmin project, an Admin interface for raspberry pi
#-
#--------------------------------------------------------------------------------------------

# -------------
# Import lib
# -------------

import re
import random
import string


# -------------
# Main object
# -------------

class httpsecurity:
	# compiled security rules
	_vartyperule={}

	# Compile security rules
	def __init__(self):
		# Vartype and associated regexp
		vartyperule={'str':'.*',
			     'date':'^[0-9]{2,4}[\/\-][0-9]{2}[\/\-][0-9]{2,4}$',
			     'alphanum':'^[0-9a-zA-Z _]*$',
                             'ldap':'^[a-zA-Z0-9]*$',
                             'email':'^[a-zA-Z0-9\-\_\.]*\@[a-zA-Z0-9\-\_]*\.[a-zA-Z]{2,3}$',
                             'id':'^[0-9]*$',
                             'num':'^-?[0-9]*$',
			     'base64':'^[A-Za-z0-9+/]*=?=?$',
			     'filename': '^[A-Za-z0-9-_,\s\.]+',
			     '|file': 'NO INSPECT'
			    }
		# Compile regexp
		for vartype in vartyperule.keys():
			if vartype[0]!='|': #type beginning by | are not inspected (used for upload file)
				self._vartyperule[vartype]=re.compile(vartyperule[vartype])
			else:
				self._vartyperule[vartype[1:]]=vartyperule[vartype]

		self._retype=type( self._vartyperule['str'])

	# Return an error
	def geterror(self,num):
		error={0:'No Error',1:'No variable type',2:'Unknown type',3:'Variable does not respect security rules',5:'Post token not found',6:'Post Token not valid'}
		if num in error.keys():
			return error[num]
		return 'Unknown error'

	# Analyze a list of variable
	def checkhttpvars(self,httpvars):
		# if no vars, escape
		if httpvars==None:
			return 0

		# Browse the tab
		for var in httpvars.keys():
			varsplit=var.split('_',1)

			# a varible name must be composed of two parts : vartype_varname
			if len(varsplit)!=2:
				return 1

			varname=varsplit[1]
			vartype=varsplit[0]

			# If unknown vartype, escape
			if not vartype in self._vartyperule:
				return 2
			# Analyze vars and check if they match the associated regexp
			if type(httpvars[var])==str:
				if type(self._vartyperule[vartype])==self._retype:
					if httpvars[var]!="" and not self._vartyperule[vartype].match(httpvars[var]):
						return 3
			elif type(httpvars[var]) in [list,tuple]:
				for item in httpvars[var]:
					if item!="" and not self._vartyperule[vartype].match(item):
						return 3
		return 0

	# A form post must include a token (stored in session vars)
	# This token is a protection againt csrf attacks because it cannot be guess by the bad guy
	# This routine just check if the sent token is the good one
	def checkposttoken(self,httpvars,sessionvars):
                if not 'alphanum_token' in httpvars.keys():
                	return 5

		if httpvars['alphanum_token']!=sessionvars['posttoken']:
			return 6
		return 0
	# Generate a new token
	def generateposttoken(self):
		return ''.join(random.choice(string.ascii_letters+string.digits) for x in range(30))
