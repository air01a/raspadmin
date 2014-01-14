import ConfigParser
import grp
import json
import base64
import os
from ..lib import loadtpl

class SambaManager:
	def __init__(self,webconf):
		self._webconf=webconf
		config = ConfigParser.ConfigParser()
		config.readfp(open('/etc/raspadmin/nassamba.conf'))
		self._basedir=config.get("SHARE", "basedir")
		self._sambaconffile=config.get("SHARE", "sambaconffile")
		self._sambatplglobal=config.get("SHARE", "templateglobal")
		self._sambatplshare=config.get("SHARE", "templateshare")
		self._serverdescription=config.get("SHARE", "serverdescription")
		self._workgroup=config.get("SHARE", "workgroup")
		self._netbiosname=config.get("SHARE", "netbiosname")
		self._dbfile=config.get("SHARE","dbfile")
                config.readfp(open('/etc/raspadmin/nasuser.conf'))
                self._nasgroup=config.get("USERS", "nasgroup")
		self.read_db()
		self.clean_db()

	def get_nas_user(self):
                users=[]
                tmp=grp.getgrnam(self._nasgroup).gr_mem
                for user in tmp:
                        users.append(user)

                return users

	def get_base_dir(self):
		return self._basedir

	def load_global_tpl(self):
		vars={}
		vars['@workgroup']=self._workgroup
		vars['@serverstring']=self._serverdescription
		vars['@netbiosname']=self._netbiosname
		vars['@nasgroup']=self._nasgroup
		return loadtpl.load_tpl(self._sambatplglobal,vars)

	def load_share_tpl(self,share):
		vars={}

		vars['@name']=share['name']
		vars['@sharepath']=share['path']
		vars['@sharecomment']=share['comment']
		vars['@sharero']='yes' if share['readonly'] else 'no'
		vars['@sharepublic']='yes' if share['public'] else 'no'
		vars['@sharewriteable']='yes' if share['writable'] else 'no'
		vars['@shareuserwrite']=share['writelist'] if share['writelist']!='' else 'None'
		vars['@sharereaduser']=share['validusers'] if share['validusers']!='' else 'None'
		return loadtpl.load_tpl(self._sambatplshare,vars)

	def find_share_from_path(self,path):
        	for i in range(0,len(self._internaldb)):
			if self._internaldb[i]['path']==path:
				return self._internaldb[i]
		return None

	def clean_db(self):
		user=self.get_nas_user()
		for share in range(len(self._internaldb)):
			validuser=self._internaldb[share]['validusers'].split(',')
			writeuser=self._internaldb[share]['writelist'].split(',')
			self._internaldb[share]['validusers']=','.join(i for i in validuser if i in user)
         		self._internaldb[share]['writelist']=','.join(i for i in writeuser  if i in user)
	

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

	def read_db(self):
		db=open(self._dbfile,"r")
		self._internaldb=json.loads(db.read())
		return 0

	def get_db(self):
		ret=[]
		for i in self._internaldb:
			i['b64path']=base64.b64encode(i['path'])
			ret.append(i)
		return ret

	def delete_share(self,name):
		found=False
		for i in range(0,len(self._internaldb)):
			if self._internaldb[i]['name']==name:
				del self._internaldb[i]
				found=True
				break
		if not found:
			return 10
		return self.write_db()


	def add_share(self, name, path, comment,readonly, public, writable, writelist, validusers):
		for share in self._internaldb:
			if share['name']==name:
				return 41
			if share['path']==path:
				return 43

		self._internaldb.append({'name':name, 'path':path, 'comment':comment,'readonly':readonly,'public':public,'writable':writable,'writelist':writelist,'validusers':validusers})
		return self.write_db()

	def modify_share(self, name, path, comment,readonly, public, writable, writelist, validusers, create=False):
		found=False

		for i in range(0,len(self._internaldb)):
			if self._internaldb[i]['path']==path:
				found=True
				indice=i
				break
		
		if not found:
			if create:
				return self.add_share(name, path, comment,readonly, public, writable, writelist, validusers)
			else:
				return 42

		self._internaldb[i]['name']=name
		self._internaldb[i]['comment']=comment
		self._internaldb[i]['readonly']=readonly
		self._internaldb[i]['public']=public
		self._internaldb[i]['writable']=writable
		self._internaldb[i]['writelist']=writelist
		self._internaldb[i]['validusers']=validusers

		return self.write_db()

	def write_samba_config(self):
		header=self.load_global_tpl()
		shareconfig=""
		for share in self._internaldb:	
			shareconfig += self.load_share_tpl(share)
		try:
			smbfile=open(self._sambaconffile,"w+")
			smbfile.write(header)
			smbfile.write(shareconfig)
			smbfile.close()
		except:
			return 60

		return os.system("killall -SIGHUP smbd")

	def get_error_str(self,error):
		errorstr={0:'No Error',10:'Unknown share',41:'Error :  share name exists',50:'Error Writing db', 60:'Error writing samba config file',42:'Share does not exist',43:'Share path exists'}
		if error in errorstr.keys():
			return errorstr[error]
		return 'Unknow error'

def main():
	sambamanager=SambaManager('')
	#print sambamanager.get_error_str(sambamanager.add_share('testi7','test7','comment',True,False,True,'1,2','1,2'))
	sambamanager.read_db()
	print sambamanager.get_db()
	sambamanager.clean_db()
	print sambamanager.get_db()

	#print sambamanager.write_samba_config()

if __name__ == '__main__':
        main()
