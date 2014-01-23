from .. import WebStructure 
import ConfigParser
import time, hmac, hashlib, json

class WebManager(WebStructure.WebAbstract):
	def __init__(self,webconf):
		self.webconf=webconf
		config = ConfigParser.ConfigParser()
                config.readfp(open(webconf['confdir']+"/gateone.conf"))
                self._port=config.get("GATEONE", "port")
		self._apikey=config.get("GATEONE", "apikey")
		self._user=config.get("GATEONE", "user")
		self._secret=config.get("GATEONE", "secret")
		self._autoconnectUrl=config.get("GATEONE","autoconnectUrl")

	def getjsonauth(self):
		secret = self._secret
		authobj = {
    			'api_key': self._apikey,
    			'upn': self._user,
    			'timestamp': str(int(time.time() * 1000)),
    			'signature_method': 'HMAC-SHA1',
    			'api_version': '1.0'
		}
		hash = hmac.new(secret, digestmod=hashlib.sha1)
		hash.update(authobj['api_key'] + authobj['upn'] + authobj['timestamp'])
		authobj['signature'] = hash.hexdigest()
		valid_json_auth_object = json.dumps(authobj)
		return valid_json_auth_object

	def get_html(self,http_context):
		template=['header.tpl','gateone/gateone.tpl','footer.tpl']
		servername=http_context.servername
		servername=servername.split(':')[0]
		includefile='gateone/headergateone.html'
		content={'jsonauth':self.getjsonauth(),'includefile':includefile,'servername':servername,'port':self._port,'autoconnect':self._autoconnectUrl}
		return WebStructure.HttpContext(statuscode=200,content=content,template=template,mimetype='text/html')

        def get_module_name(self):
                return "SSH"

