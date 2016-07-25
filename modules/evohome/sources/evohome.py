import ConfigParser
from evohomeclient2 import EvohomeClient
import sqlite3
import time,datetime

class EvoHome:

	def __init__(self):
		config = ConfigParser.ConfigParser()
		config.readfp(open('/etc/raspadmin/evohome.conf'))
		self.login=config.get("EVOHOME", "login")
		self.password=config.get("EVOHOME", "password")
		self.dbname=config.get("EVOHOME","dbname")
		
		self.ec = EvohomeClient(self.login, self.password)
		
	def getCurrentValues(self):
		temperatures=[]
		for device in self.ec.temperatures():
			temperatures.append({'name':device['name'],'temperature':device['temp']})
		return temperatures
	
        def getHistory(self):
                now = time.time()
                first = now - 86400
                conn = sqlite3.connect(self.dbname)
                cursor = conn.cursor()
                cursor.execute("SELECT DISTINCT name FROM data ORDER BY name ASC")
                names = cursor.fetchall()

                results={}

                cursor.execute("SELECT time FROM data WHERE time>? AND time<?",(first,now))
                allDates = cursor.fetchall()
                hours = []
                for date in allDates:
                        hour = datetime.datetime.fromtimestamp(date[0]).hour
                        if hour not in hours:
                                hours.append(hour)

                for row in names:
                        result={}
                        cursor.execute("SELECT name,temp,time FROM data WHERE name=? AND time>? AND time<? ORDER BY time ASC",(row[0],first,now))
                        data = cursor.fetchall()
                        for captor in data:
                                result[datetime.datetime.fromtimestamp(captor[2]).hour] = captor[1]
                        results[row[0]]=result
                results["base_hours"]=hours
                return results

