#---------------------------------------------------------------------------------------------
#-
#- status.py
#- ---------------
#-
#- Get system information to display on status page
#-
#- Author : Erwan Niquet
#- Date : Jan 2014
#- Part of raspadmin project, an Admin interface for raspberry pi
#-
#--------------------------------------------------------------------------------------------

# -------------
# Import lib
# -------------



import psutil
import subprocess
import socket
import os
import time
from netifaces import interfaces, ifaddresses, AF_INET

def getHostName():
	return socket.gethostname()

def getIP():
	ip_list = []
    	for interface in interfaces():
		try:
        		for interface in ifaddresses(interface)[AF_INET]:
				if not interface['addr'].startswith("127."):
					ip_list.append(interface['addr'])
		except:
			pass
    	return ip_list

#	return [ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")][:1]

def getCpu():
	return psutil.cpu_times()

def getCpuPercent():
	cpu=getCpu()
	total= cpu.user + cpu.nice + cpu.system + cpu.idle + cpu.iowait + cpu.irq + cpu.softirq

	user = int(100*cpu.user / total)
	nice = int(100*cpu.nice / total)
	system = int(100*cpu.system / total)
	idle = int(100*cpu.idle / total)
	iowait =  int(100*cpu.iowait / total)
	irq = int(100*cpu.irq / total)
	softirq = int(100*cpu.softirq / total)

	return {'user':user,'nice':nice,'system':system,'idle':idle,'iowait':iowait,'irq':irq,'softirq':softirq }



def getNumCpu():
	return psutil.NUM_CPUS

def getCPUusage():
	return psutil.cpu_percent(percpu=True)

def getPartitions():
	return psutil.disk_partitions()	

def getDiskUsage(mountpoint):
	return psutil.disk_usage(mountpoint)

def getMemory():
	memory=psutil.virtual_memory()

	total = getDisplayValue(memory.total)
	available = getDisplayValue(memory.available)
	availableraw=memory.available
	used = getDisplayValue(memory.used)
	usedraw = memory.used
	percent = int(memory.percent)
	buffers = getDisplayValue(memory.buffers)
	bufferraw = memory.buffers
	free = getDisplayValue(memory.free)
	freeraw = memory.free
	memory=psutil.swap_memory()
        swtotal = getDisplayValue(memory.total)
        swused = getDisplayValue(memory.used)
        swpercent = int(memory.percent)
	swfree = getDisplayValue(memory.free)
	
	return {'usedraw':usedraw,'bufferraw':bufferraw,'freeraw':freeraw,'total':total,'available':available,'used':used,'percent':percent,'buffers':buffers,'free':free,'swfree':swfree,'swtotal':swtotal,'swpercent':swpercent}
	
def getUptime(text=False):
	bt=int(time.time()-psutil.get_boot_time())
	if not text:
		return bt
	day=int(bt/86400)
	bt-=day*86400
	hour=int(bt/3600)
	bt-=hour*3600
	minute=int(bt/60)
	seconde=int(bt-minute*60)
	return "%id %ih %im %is" % (day,hour,minute,seconde)


def getTemperature():
	try:
        	s = subprocess.check_output(["/usr/bin/vcgencmd","measure_temp"])
		return float(s.replace("temp=","").replace("'C\n",""))
    	except:
        	return 0

def getCpuFrequency():
        try:
                s = subprocess.check_output(["/usr/bin/vcgencmd","measure_clock arm"])
                return int(s.split("=")[1].replace("'C\n",""))
        except:
                return 0



def getDisplayValue(value):
	if value>(1024*1024*1024):
		return str(int(value/(1024*1024*1024)))+" Gb"

        if value>(1024*1024):
                return str(int(value/(1024*1024)))+" Mb"

        if value>(1024):
                return str(int(value/(1024)))+" kb"
	
	return str(int(value))+" b"



def getDiskSummary():
	summary=[]
	partitions=getPartitions()
	for partition in partitions:
		device=partition.device
		mountpoint=partition.mountpoint
		fstype=partition.fstype
		
		space=getDiskUsage(mountpoint)
		total= getDisplayValue(space.total)
		free = getDisplayValue(space.free)
		used = getDisplayValue(space.used)
		percent = int(space.percent)
		summary.append({ 'device':device,'mountpoint':mountpoint,'fstype':fstype,'total':total,'free':free,'used':used,'percent':percent})

	return summary

def getLoadAvg():
	tab=os.getloadavg()
	return {'la1':tab[0],'la2':tab[1],'la3':tab[2]}
