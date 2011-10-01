import time
import threading
import subprocess
import re

def stop_mtrackgateway():
    output = subprocess.Popen("ps -f -a | grep \"python manage.py data_processor\" | grep -v \"grep\" | grep -v \"bin/sh\"", stdout=subprocess.PIPE, shell=True).stdout.read()
    m = re.search("root[ ]+([0-9]+)",output)
    try:
        pid = int(m.group(1))
        output = subprocess.Popen("kill " + str(pid), stdout=subprocess.PIPE, shell=True).stdout.read()
        print output
    except:
        pass
    #	output = subprocess.Popen("net stop \"Arena Maxtrack Gateway\"", stdout=subprocess.PIPE, shell=True).stdout.read()
def start_mtrackgateway():
    subprocess.Popen("python manage.py data_processor", stdout=subprocess.PIPE, shell=True)

class Timer(threading.Thread):
	def __init__(self, seconds):
		self.runTime = seconds
		threading.Thread.__init__(self)
	def run(self):
		while True:
			stop_mtrackgateway()
			start_mtrackgateway()
			time.sleep(self.runTime)

t = Timer(600)
t.start()

