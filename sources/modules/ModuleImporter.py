import os
import sys
moduledir="/root/python/modules/"

class ModuleImporter:
	_modulelist={}	
	_modulerequired=[]

	def __init__(self,moduleconf):
		sys.path.insert(0,moduleconf['moduledir'])
		self.moduledir=moduleconf['moduledir']
		self.conf=moduleconf

	def loadmodulelist(self,submodule,conf):
		modules=[module for module in os.listdir(self.moduledir) if (os.path.isdir (os.path.join(self.moduledir,module)))]
		for module in modules:
        		modulefile=os.path.join(self.moduledir,module,submodule+'.py')
        		if (os.path.isfile(modulefile)):
#				try:
                			pythonsubmodule='modules.'+module+'.'+submodule
					moduleptr= __import__(pythonsubmodule,globals(), locals(), [submodule] )
					obj=moduleptr.WebManager(conf)

					if obj.is_required()==True:
						if obj.priority()!=None:
							self._modulerequired[0:0]=[obj]
						else:
							self._modulerequired.append(obj)
					else:
						self._modulelist[module]=obj
					print "+++ Module %s has been imported" % (module)
#				except:
					print "--- Error Importing module" + module
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
		

	def moduleexists(self,module):
		if module in self._modulelist.keys():
			return True
		return False

	def getrequiredmodules(self):
		return self._modulerequired

	def getmodule(self,module):
		if (self.moduleexists(module)==True):
			return  self._modulelist[module]
		               		
	
	def getmodulelist(self):
#		return [{'name':self._modulelist[mod].get_module_name(),'link':mod} for mod in self._modulelist.keys() if self._modulelist[mod].get_module_name()!=""]
		return self._modulelistordered			

