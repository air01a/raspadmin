import os, sys
from stat import *
import base64
from shutil import copy,copy2,copytree,move,rmtree

class FileManager:

	def __init__(self,basepath):
		self._basepath=basepath.split(',')


        def get_format_size(self,number):
                extension = [ 'b', 'Kb', 'Mb','Gb' ]
                for i in range(len(extension)):
                        if number/1024<1:
                                return str(round(number,2))+ " " + extension[i]
                        else:
                                number=number/1024+0.0
                return str(round(number*1024,2))+" "+"Gb"



	def path_decode(self,path):
		return base64.b64decode(path)

	def get_error(self,error):
		errorstr={0:'No Error',1:'Path not in restricted path',11:'Invalid path',12:'Directory creation failed',13:'File copy failed',14:'File moved failed',15:'Directory copy failed',16:'rm_tree failed'}

		if error in errorstr.keys():
			return errorstr[error]
		return "Unknown error"


	def list_file_from_path(self,path):
		filelist=[]
		completepath=os.path.abspath(path)
                if not self.validate_path(path):
			return []

                for f in os.listdir(completepath):
			pathname = os.path.join(completepath, f)
		
                        try:
                                stats = os.stat(pathname)
				mode=stats.st_mode
				size=self.get_format_size(stats.st_size)
                                if not S_ISDIR(mode):
                                        filelist.append({'pathname':os.path.basename(pathname),'link':base64.b64encode(pathname),'size':size})
                        except:
                                pass
                return filelist


	def validate_path(self,path):
		path=os.path.abspath(path)
                for vp in self._basepath:
                        if path.startswith(vp):
                        	return True 
		return False	

	def list_dir_from_path(self,path):
    		filelist=[]
		completepath=os.path.abspath(path)

		if not self.validate_path(path):
			for vd in self._basepath:
				filelist.append({'pathname':os.path.basename(vd),'link':base64.b64encode(vd)})
			return filelist

		filelist.append({'pathname':'..','link':base64.b64encode(os.path.abspath(completepath+'/..'))})

		for f in os.listdir(completepath):
        		pathname = os.path.join(completepath, f)
			try:
	        		mode = os.stat(pathname).st_mode
        			if S_ISDIR(mode):
					filelist.append({'pathname':os.path.basename(pathname),'link':base64.b64encode(pathname)})
			except:
				pass
    		return filelist

	def make_dir(self,path):
		if not self.validate_path(path):
			return 11
		try: 
			os.makedirs(path)
		except:
			return 12
		return 0

	def file_copy(self,src,dst,keepmeta=False):
		if not self.validate_path(src) or not self.validate_path(dst):
			return 11

		try:
			if keepmeta:
				copy2(src,dst)
			else:
				copy(src,dst)
		except:
			return 13

		return 0
		
	def file_move(self,src,dst):
		if not self.validate_path(src) or not self.validate_path(dst):
                        return 11
		try:
			move(src,dst)
		except:
			return 14
		return 0

	def dir_copy(self,src,dst,symlink=False,ignore=None):
		if not self.validate_path(src) or not self.validate_path(dst):
                        return 11
		try:
			copytree(src,dst,symlink,ignore)
		except:
			return 15
		return 0

	def rm_tree(self,path):
		if not self.validate_path(path):
			return 11
		try:
			rmtree(path)
		except:
			return 16
		return 0

	def rm_file(self,path):
		if not self.validate_path(path):
                        return 11
		try:
			os.remove(path)
		except:
			return 17
		return 0 


def main(args):
	if len(args)>1:
		filemanager=FileManager(os.path.abspath('.,/home'))
		if args[1]=='base64' and len(args)>2:
			path=filemanager.path_decode(args[2])
		else:
			path=args[1]
		print filemanager.list_dir_from_path(path)

if __name__ == '__main__':
	main(sys.argv)
