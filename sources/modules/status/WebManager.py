from .. import WebStructure 
import status


class WebManager(WebStructure.WebAbstract):
	def __init__(self,webconf):
		self.webconf=webconf

	def get_html(self,http_context):
		template=['header.tpl','status/status.tpl','footer.tpl']

		cpu=status.getCpuPercent()
		numcpu=status.getNumCpu()
		cpuusage=status.getCPUusage()
		average=0
		count=0
		for i in cpuusage:
			average+=i
			count+=1
		average=int(average/count)
		cpuusage={'average':average,'values':cpuusage}
		disk=status.getDiskSummary()
		temperature=status.getTemperature()
		memory=status.getMemory()
	
		loadavg=status.getLoadAvg()	
		hostname=status.getHostName()
	
		cpufrequency=str(status.getCpuFrequency()/1000000)+" Mhz"
		
		for d in disk:
			if d['mountpoint']=='/':
				freespace=d['free']

		uptime=status.getUptime(True)
		ip = status.getIP()
		includefile='status/headerstatus.html'
		content={'freespace':freespace,'cpufrequency':cpufrequency,'uptime':uptime,'loadavg':loadavg,'ip':ip,'hostname':hostname,'cpu':cpu,'numcpu':numcpu,'cpuusage':cpuusage,'disk':disk,'temperature':temperature,'memory':memory,'includefile':includefile}	
		return WebStructure.HttpContext(statuscode=200,content=content,template=template,mimetype='text/html')

        def get_module_name(self):
                return "Status"

