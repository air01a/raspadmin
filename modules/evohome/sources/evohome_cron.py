import ConfigParser
from evohomeclient2 import EvohomeClient
import sqlite3
import time

config = ConfigParser.ConfigParser()
config.readfp(open('/etc/raspadmin/evohome.conf'))
login=config.get("EVOHOME", "login")
password=config.get("EVOHOME", "password")
dbname=config.get("EVOHOME","dbname")

date = time.time()

conn = sqlite3.connect(dbname)
cursor = conn.cursor()

ec = EvohomeClient(login, password)
for device in ec.temperatures():
	#cursor.execute("""INSERT INTO users(name, age) VALUES(?, ?)""", ("olivier", 30))
	name=device['name']
	temp=device['temp']+0.0
	#print name+" "+str(temp)+" "+str(date)
	cursor.execute("INSERT INTO data(name,temp,time) VALUES(?,?,?)",(name,temp,date))
conn.commit()
