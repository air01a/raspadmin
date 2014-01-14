import os, sys
from stat import *
import base64


class FileManager:

	def __init__(self,basepath):
		self._basepath=basepath.split(',')

	def path_decode(self,path):
		return base64.b64decode(path)

	def get_error(self,error):
		errorstr={0:'No Error',1:'Path not in restricted path'}

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
                                mode = os.stat(pathname).st_mode
                                if not S_ISDIR(mode):
                                        filelist.append({'pathname':os.path.basename(pathname),'link':base64.b64encode(pathname)})
                        except:
                                pass
                return filelist


	def validate_path(self,path):
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
