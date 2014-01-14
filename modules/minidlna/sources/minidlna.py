import os
import sys
import ConfigParser
import subprocess 
from time import sleep
from ..lib import process
import json
from ..lib import loadtpl
import base64

class MiniDlna:
	def __init__(self, conf):
		self._conf = conf
		config = ConfigParser.ConfigParser()
                config.readfp(open('/etc/raspadmin/minidlna.conf'))
                self._dbfile=config.get("MINIDLNA", "dbpath")
		self._forcereload=config.get("MINIDLNA", "forcereload").split(' ')
		self._stop=config.get("MINIDLNA", "stop").split(' ')
		self._start=config.get("MINIDLNA", "start").split(' ')
		self._check=config.get("MINIDLNA", "check").split(' ')
		self._minidlnatplshare=config.get("MINIDLNA", "tpl")
		self._dlnaconffile=config.get("MINIDLNA", "conffile")
		self.read_db()

        def write_db(self,vars=None):
                if vars==None:
                        vars=self._internaldb
                jsondb=json.dumps(vars)
                try:
                        db=open(self._dbfile,"w+")
                        db.write(jsondb)
                        db.close()
                except:
                        return 50
                return 0

	def write_config(self):
		strshare=""
		for share in self._internaldb:
			strshare+="media_dir="
			if share['type']=='music':
				strshare+='A,'
			elif share['type']=='photo':
				strshare+='P,'
			elif share['type']=='video':
				strshare+='V,'	
			strshare+=share['path']+"\n"
		config=loadtpl.load_tpl(self._minidlnatplshare,{'@media_dir':strshare})
                try:
                        dlnafile=open(self._dlnaconffile,"w+")
                        dlnafile.write(config)
                        dlnafile.close()
                except:
                        return 60
		return 0
	
        def read_db(self):
                db=open(self._dbfile,"r")
		try:
                	self._internaldb=json.loads(db.read())
			db.close()
		except:
			self._internaldb=[]
                return 0


	def check_status(self):
		retcode=process.execute(self._check)
		return retcode

	def start(self):
		retcode=process.execute(self._start)
		return retcode

	def stop(self):
		retcode=process.execute(self._stop)
		return retcode

	def reload(self):
		retcode=process.execute(self._forcereload)
		return retcode

	def add_share(self,path,sharetype):
		for i in self._internaldb:
			if i['path']==path and i['type']==sharetype:
				return 40
		self._internaldb.append({'path':path,'type':sharetype})
		return 0
		
	def delete_share(self,path,sharetype):
		for i in range(len(self._internaldb)):
			if self._internaldb[i]['path']==path and self._internaldb[i]['type']==sharetype:
				del self._internaldb[i]
				return 0
		return 10
	
	def get_shares(self):
		ret=[]
                for i in self._internaldb:
                        i['b64path']=base64.b64encode(i['path'])
                        ret.append(i)
                return ret

	def get_error(self,errorcode):
		errorstr={0:'No Error',10:'Share not found',40:'Share already exists'}

		if errorcode in errorstr.keys():
			return errorstr[errorcode]
		return 'Unknown error'

