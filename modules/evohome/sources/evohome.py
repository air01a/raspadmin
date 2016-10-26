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
		self.extemp=config.get("EVOHOME", "extemp")
		if self.extemp=="True":
		        self.apikey=config.get("EVOHOME", "apikey")
		        self.city=config.get("EVOHOME", "city")

		
	def getCurrentValues(self):
		ec = EvohomeClient(self.login, self.password)
		temperatures=[]
		weather=None
		for device in ec.temperatures():
			temperatures.append({'name':device['name'],'temperature':device['temp']})
		if self.extemp=="True":
			import pyowm
		        owm = pyowm.OWM(self.apikey)
        		observation = owm.weather_at_place(self.city)
        		w = observation.get_weather()
			weather={}
			weather['temperature']=w.get_temperature('celsius')['temp']
			weather['min']=w.get_temperature('celsius')['temp_min']
			weather['max']=w.get_temperature('celsius')['temp_max']
			weather['rain']=w.get_rain()
			weather['cloud']=w.get_clouds()
			weather['wind']=w.get_wind() 
			weather['humidity']=w.get_humidity()
			weather['pressure']=w.get_pressure()
			weather['status']=w.get_detailed_status()
			weather['icon']='https://openweathermap.org/img/w/'+w.get_weather_icon_name()+'.png'
			sunrise=datetime.datetime.fromtimestamp(w.get_sunrise_time()).strftime("%Hh%M")
			weather['sunrise']=sunrise
			sunset = datetime.datetime.fromtimestamp(w.get_sunset_time()).strftime("%Hh%M")
			weather['sunset']=sunset

		return (temperatures,weather)
	
        def getHistory(self):
                now = time.time()
                first = now - 86400
                conn = sqlite3.connect(self.dbname)
                cursor = conn.cursor()
                cursor.execute("SELECT DISTINCT name FROM data ORDER BY name ASC")
                names = cursor.fetchall()

                results={}

                cursor.execute("SELECT time FROM data WHERE time>? AND time<=?",(first,now))
                allDates = cursor.fetchall()
                hours = []
                for date in allDates:
                        hour = datetime.datetime.fromtimestamp(date[0]).hour
                        if hour not in hours:
                                hours.append(hour)

                for row in names:
                        result={}
                        cursor.execute("SELECT name,temp,time FROM data WHERE name=? AND time>? AND time<=? ORDER BY time ASC",(row[0],first,now))
                        data = cursor.fetchall()
                        for captor in data:
                                result[datetime.datetime.fromtimestamp(captor[2]).hour] = captor[1]
                        results[row[0]]=result
                results["base_hours"]=hours
                return results

