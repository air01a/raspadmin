import os
import crypt
from getpass    import getpass
import subprocess
import pwd
from time import sleep 
import grp
import ConfigParser
import random
import string

class ManageUser:

	def __init__(self,config):
		self._config=config
		config = ConfigParser.ConfigParser()
                config.readfp(open('/etc/raspadmin/nasuser.conf'))
		self._loginscript=config.get("USERS", "loginscript")
		self._nasgroup=config.get("USERS", "nasgroup")
		self._home=config.get("USERS", "home")

	def execute(self,cmd,input=None,output=None):
                p = subprocess.Popen(cmd, stdin=subprocess.PIPE,stderr=subprocess.STDOUT)
		if input!=None:
	                p.stdin.write(input)
	                p.stdin.flush()
		
                for x in range(0, 20):
                        if p.poll() is not None:
                                break
                        sleep(0.5)
                else:
                        p.terminate()
                        sleep(1)
                        p.kill()
			return 21

		return p.returncode
		
	def createUser(self,name,username,password):

		tmppass=''.join(random.choice(string.ascii_letters+string.digits) for x in range(30))
    		encPass = crypt.crypt(tmppass,"22")   
    		ret=os.system("useradd -G "+self._nasgroup+" -p "+encPass+ " -s "+ " "+ self._loginscript + " -d "+ self._home + " -m "+ " -c \""+ username+"\" " + name)
		if ret!=0:
			return ret
		return self.set_password(name,password,True)
	
	def set_password(self,user, password, new=False):
    		PASSWD_CMD='/usr/bin/smbpasswd'
   		if new:
			cmd = [PASSWD_CMD, '-s','-a',user]
		else:
			cmd = [PASSWD_CMD, '-s',user]
		strstdin=u'%(p)s\n%(p)s\n' % { 'p': password }

		return 20*self.execute(cmd,strstdin)	

	def list_user(self,startwith=None):
    		user=[]
    		for p in pwd.getpwall():
			if startwith!=None:
				if p.pw_gecos.startswith(startwith):
					user.append(p)
			else:
				user.append(p)
    		return user

	def get_user(self,user):
		return pwd.getpwnam(user)

	def del_user(self,user):
		
                PASSWD_CMD='/usr/bin/smbpasswd'
                cmd = [PASSWD_CMD, '-x',user]
                p = self.execute(cmd)

                if p!=0:
                        return p

    		cmd=['/usr/sbin/userdel',user]
    		p = self.execute(cmd) 
                return 20*p



	def usergroup_fromid(self,groupid):
		return grp.getgrgid(groupid)

	def usergroup_fromname(self,name):
			return grp.getgrnam(name)

	def usergroup_getall(self):
    		return grp.getgrall()

	def get_error(self,error):
		errorcode={0:'No Error',21:'system command hang',8:'User is currently used by a process',2304:'User exists'}
		if error in errorcode.keys():
			return errorcode[error]
		return "Unknow error"

	def get_nas_user(self):
		users=[]
		tmp=self.usergroup_fromname(self._nasgroup).gr_mem
		for user in tmp:
			users.append(self.get_user(user))

		return users
			


def main():
	#set_password('test',"azerty'; echo 1 > /tmp/test;")
	manageuser=ManageUser('test')
	#manageuser.createUser("test3","test3","asjdjkldjzdzkljjlzkd")
	#users=manageuser.usergroup_fromname("NAS").gr_mem

	#for user in users:
	#	print manageuser.get_user(user)
	

	#print usergroup_fromid(usergroup_fromname('root').gr_gid)
	#print manageuser.del_user('test3')

if __name__ == '__main__':
       	main()

