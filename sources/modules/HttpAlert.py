import WebStructure

def httpalert(alert,status=200):
	return WebStructure.HttpContext(statuscode=status,content={'error':alert},template='httpalert.tpl',mimetype='text/html')  
