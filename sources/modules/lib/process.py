import subprocess
from time import sleep
import os

def execute(cmd,input=None,output=None):
	_devnull=None
	if output==None:
                _devnull=open(os.devnull, 'wb')
		output = _devnull

	p = subprocess.Popen(cmd, stdin=subprocess.PIPE,stderr=subprocess.STDOUT,stdout=output)
        if input!=None:
        	p.stdin.write(input)
                p.stdin.flush()
	for x in range(0, 20):
        	if p.poll() is not None:
                	break
		sleep(0.5)
	else:
		if _devnull!=None:
			_devnull.close()
		p.terminate()
		sleep(1)
                p.kill()
                return 21

	if _devnull!=None:
		_devnull.close()
	return p.returncode

