class HttpContext:
	def __init__(self,**kwds):
		self.__dict__.update(kwds)

	def addVar(self,name,value):
		self.__dict__.update({name:value})

	def hasVar(self,name):
		if name in self.__dict__.keys():
			return True
		return False

class WebAbstract:
	def __init__(self):
		raise NotImplementedError()

	def get_html(self,http_context):
		raise NotImplementedError()
	
	def is_required(self):
		return False

	def get_module_name(self):
		raise NotImplementedError()

	def priority(self):
		return None
