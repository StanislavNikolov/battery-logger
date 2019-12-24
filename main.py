import time
import pyscreenshot
from PIL import Image
import os

import csv as csvlib

class Measurement:
	def __init__(self, current, voltage):
		self.time = time.time()

		self.current = current
		self.voltage = voltage
		self.power = self.current * self.voltage

		# should be enough to determine what was the user doing, but without specifics
		# e.g. youtube, reading, coding
		#SCALE = 4
		#self.screenshot = pyscreenshot.grab()
		#scr_scaled_size = ( self.screenshot.size[0] // SCALE, self.screenshot.size[1] // SCALE )
		#self.screenshot = self.screenshot.resize(scr_scaled_size)

		self.focused_window = os.popen('./get_focused_window_class.py').read().strip()

	def __str__(self):
		return f'[{self.time}]: {self.power:.2f}W {self.current:.2f}A {self.voltage:.2f}V ({self.focused_window}'

def measure():
	current = float(open('/sys/class/power_supply/BATT/current_now').read()) / 1e6
	voltage = float(open('/sys/class/power_supply/BATT/voltage_now').read()) / 1e6
	return Measurement(current, voltage)

csvfile = open('data.csv', mode='a')
csv_writer = csvlib.writer(csvfile, delimiter=',', quotechar='"', quoting=csvlib.QUOTE_MINIMAL)

while True:
	time.sleep(2)

	begin = time.time()

	M = measure()
	#M.screenshot.save('asd.png')
	csv_writer.writerow([M.time, M.power, M.current, M.power, M.focused_window])
	print(M)

	end = time.time()

	timediff = (end - begin)
	#print(f'took {timediff*1000:.2f}ms')
