import datetime
import time
import pyscreenshot
from PIL import Image
import os
import io
import sqlite3

db_conn = sqlite3.connect('measurements.sqlite3')

class Measurement:
	def __init__(self, time, current, voltage, batt_charge, batt_status, focused_window, screenshot = None):
		self.time = time
		self.current = current
		self.voltage = voltage
		self.batt_charge = batt_charge
		self.batt_status = batt_status
		self.power = self.current * self.voltage
		self.focused_window = focused_window
		self.screenshot = screenshot

	def __str__(self):
		return f'[{self.time}]: {self.power:.2f}W {self.current:.2f}A {self.voltage:.2f}V - {self.batt_status} - ({self.focused_window})'

def measure(take_screenshot = False):
	# https://www.kernel.org/doc/Documentation/power/power_supply_class.txt
	curr_time = datetime.datetime.now()
	charge  = float(open('/sys/class/power_supply/BATT/charge_now').read()) / 1e6
	current = float(open('/sys/class/power_supply/BATT/current_now').read()) / 1e6
	voltage = float(open('/sys/class/power_supply/BATT/voltage_now').read()) / 1e6
	status  =       open('/sys/class/power_supply/BATT/status').read().strip()

	focused_window = os.popen('./get_focused_window_class.sh').read().strip()

	if take_screenshot:
		# should be enough to determine what was the user doing, but without specifics
		# e.g. youtube, reading, coding
		SCALE = 0.25
		scr = pyscreenshot.grab(childprocess=False, backend = "mss")
		scaled_size = (int(scr.size[0] * SCALE), int(scr.size[1] * SCALE))
		scr = scr.resize(scaled_size, Image.NEAREST)
	else:
		scr = False

	return Measurement(curr_time, current, voltage, charge, status, focused_window, scr)

cnt = 0
while True:
	begin = time.time()

	take_screenshot = True if cnt % 5 == 0 else False

	M = measure(take_screenshot)
	print(M)

	if take_screenshot:
		stream = io.BytesIO()
		M.screenshot.save(stream, format = 'jpeg', quality = 80)
		screenshot_bytes = stream.getvalue()
		print(len(screenshot_bytes) / 1000)
	else:
		screenshot_bytes = None

	cur = db_conn.cursor()
	cur.execute("""
		INSERT INTO measurements (time, current, voltage, battery_charge, battery_status, focused_window, screenshot)
		VALUES (?, ?, ?, ?, ?, ?, ?)""",
		(M.time, M.current, M.voltage, M.batt_charge, M.batt_status, M.focused_window, screenshot_bytes)
	)
	db_conn.commit()

	end = time.time()

	timediff = (end - begin)
	print(f'took {timediff*1000:.2f}ms')

	sleep = 2.0 - timediff
	if sleep > 0: time.sleep(sleep)
	cnt += 1

