from threading import Thread
import requests 
import time
import threading
progress=[]
import sys
import urllib

class Downloader(Thread):

	def __init__(self, aToDownload): 
		Thread.__init__(self)
		self.next = False
		self.aToDownload = aToDownload
		self.bandwidth = 0

	def fileToDownload(self):
		for i in xrange(0,len(self.aToDownload)):
			sys.stdout.flush()
			if self.aToDownload[i]['state']=='w':
				self.next=i
				return True
		return False

	def run(self):
		try:
			while self.fileToDownload()!=False:
				url=self.aToDownload[self.next]['url']
				self.aToDownload[self.next]['id']=self.next
				file_name = self.aToDownload[self.next]['path']
				self.aToDownload[self.next]['state']='d'
				with open(file_name, "wb+") as f:
					response = requests.get(url, stream=True)
					total_length = response.headers.get('content-length')
					if total_length is None:
						f.write(response.content)
					else:
            					total_length = int(total_length)
						self.aToDownload[self.next]['length']=total_length
						dl = 0
						self.bandwidth = 0
						timer = time.time()
						
						for data in response.iter_content(chunk_size=4096):
							dl += len(data)
							f.write(data)
							self.aToDownload[self.next]['progression']=dl
							self.bandwidth = dl /(time.time()-timer)
						f.close()
						self.aToDownload[self.next]['state']='f'
						if file_name[-4:].lower() == '.rar':
							self.aToDownload[self.next]['rar']='t'

						self.bandwidth = 0
				
		except:
			self.aToDownload[self.next]['state']='E'
					
						
class DownloadManager():
	def __init__(self, path):
		self.aToDownload = []
		self.path = path
		self.thread = Downloader(self.aToDownload)
		self.thread.start()

	def get_format_size(self,number):
                number=float(number)
                extension = [ 'B', 'KB', 'MB','GB' ]
                for i in range(len(extension)):
                        if number/1024<1:
                                return str(round(number,2))+ " " + extension[i]
                        else:
                                number=number/1024
                return str(round(number*1024,2))+" "+"Gb"

	def addDownload(self, url):
		try:
			file_name = urllib.unquote(url[url.rfind('/') + 1:])
		except:
			self.aToDownload.append({'url':url,'path':'Error','filename':'error','state':'E','progression':0,'length':0,'id':-1,'rar':'f'})
			return
		self.aToDownload.append({'url':url,'path':self.path+'/'+file_name,'filename':file_name,'state':'w','progression':0,'length':0,'id':-1})
		if not self.thread.isAlive():
			self.thread = Downloader(self.aToDownload)
			self.thread.start()

	def updateStatus(self, filename, status):
		for line in self.aToDownload:
			if line["filename"]==filename:
				line["state"]=status
				return True
		return False
		

	def downloadStatus(self):
		ret = []

		for line in self.aToDownload[::-1]:
			i = line.copy()
			if i['length']!=0:
				i['percent'] = int(100*i['progression']/i['length'])
			else:
				i['percent'] = 0
			i['progression'] = self.get_format_size(i['progression'])
			i['length'] = self.get_format_size(i['length'])
			if i['state'] == 'd':
				i['bandwidth'] = self.get_format_size(self.thread.bandwidth) + '/s'
			ret.append(i)
			
		return ret
