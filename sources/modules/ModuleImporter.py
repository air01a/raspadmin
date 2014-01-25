#---------------------------------------------------------------------------------------------
#-
#- ModuleImporter.py
#- ---------------
#-
#- Module importer for raspadmin
#-
#- Author : Erwan Niquet
#- Date : Jan 2014
#- Part of raspadmin project, an Admin interface for raspberry pi
#-
#--------------------------------------------------------------------------------------------

# -------------
# Import lib
# -------------

import os
import sys
import traceback



# -------------
# Main Object
# -------------
class ModuleImporter:
	_modulelist={}	
	_modulerequired=[]

	# Read conf
	def __init__(self,moduleconf):
		sys.path.insert(0,moduleconf['moduledir'])
		self.moduledir=moduleconf['moduledir']
		self.conf=moduleconf

	# Load module from directory
	def loadmodulelist(self,submodule,conf):
		# List dir
		modules=[module for module in os.listdir(self.moduledir) if (os.path.isdir (os.path.join(self.moduledir,module)))]
		# Browse module
		for module in modules:
			#Check if the file WebManager.py exists
        		modulefile=os.path.join(self.moduledir,module,submodule+'.py')
        		if (os.path.isfile(modulefile)):
				try:
					# Load it
                			pythonsubmodule='modules.'+module+'.'+submodule
					moduleptr= __import__(pythonsubmodule,globals(), locals(), [submodule] )
					obj=moduleptr.WebManager(conf)
	
					# Check if this module is mandatory, as security module or login
					# Then put it in the correct list
					if obj.is_required()==True:
						if obj.priority()!=None:
							self._modulerequired[0:0]=[obj]
						else:
							self._modulerequired.append(obj)
					else:
						self._modulelist[module]=obj
					print "+++ Module %s has been imported" % (module)
				except:
					print "--- Error Importing module" + module
					print traceback.format_exc()
		# Order module according to the list in raspadmin.conf
		self._modulelistordered=[]
		modules=self._modulelist.copy()
		if 'module_order' in self.conf.keys():
			modulestab=self.conf['module_order'].split(',')
			for module in modulestab:
				if module in modules.keys():
					if self._modulelist[module].get_module_name()!="":
						self._modulelistordered.append({'name':self._modulelist[module].get_module_name(),'link':module})
					del modules[module]
		for module in modules.keys():
			if self._modulelist[module].get_module_name()!="":
				self._modulelistordered.append({'name':self._modulelist[module].get_module_name(),'link':module})
		
	# Check if a module exists or not
	def moduleexists(self,module):
		if module in self._modulelist.keys():
			return True
		return False
	# return the list of all mandatory modules
	def getrequiredmodules(self):
		return self._modulerequired

	# return the module object (according to the module name)
	def getmodule(self,module):
		if (self.moduleexists(module)==True):
			return  self._modulelist[module]
		               		
	# Get the module list
	def getmodulelist(self):
		return self._modulelistordered			

