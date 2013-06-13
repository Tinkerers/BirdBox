import threading
import time
import Queue
from video import Video
from settings import *
try:
	import RPi.GPIO as GPIO
	PI = True
except ImportError:
	PI = False
class Printer(threading.Thread):
	#----------------------------------------------------------------------
	def __init__(self, queue, logger, pi):
		threading.Thread.__init__(self)
		self.queue = queue
		self.pi = pi
		self.logger = logger
		self.logger.debug("Twitter printer created")
		self.videoQueue = Queue.PriorityQueue(1)

	#----------------------------------------------------------------------

	def blink(self):
		GPIO.output(LIGHT_PIN_1, GPIO.LOW)
		GPIO.output(LIGHT_PIN_2, GPIO.LOW)
		t0 = time.time()

		light_pins = [LIGHT_PIN_1]
		if (LIGHT_PIN_2):
			light_pins.append(LIGHT_PIN_2)

		if (LIGHT_BLINK_DELAY == 0):
			# No blinking
			for pin in light_pins:
				GPIO.output(pin, GPIO.HIGH)
				time.sleep(LIGHT_RUN_TIME)
		else:
			# blink/alternate lights
			while (time.time() - t0 < LIGHT_RUN_TIME):
				for i, pin in enumerate(light_pins):
					GPIO.output(pin, (i+1) % 2)
				time.sleep(LIGHT_BLINK_DELAY)
				for i, pin in enumerate(light_pins):
					GPIO.output(pin, i % 2)
				time.sleep(LIGHT_BLINK_DELAY)

		for pin in light_pins:
			GPIO.output(pin, GPIO.LOW)


	def run(self):
		video = None
		while True:
			# Make sure our printing thread is alive and happy
			if not video or not video.is_alive():
				self.logger.info("Starting video thread")
				video = Video(self.logger, self.videoQueue, self.queue)
				video.setDaemon(True)
				video.start()

			try:
				# Pull the message from the queue
				msg = self.queue.get()
				self.videoQueue.put(msg)
				priority = msg[0]
				line1 = msg[1]
				line2 = msg[2]
				alert = msg[3]
				t0 = time.time()

				if priority == PRIORITY_HIGH:
					self.logger.info(line1 + " " + line2)
				
				# If we should turn the light on, do it
				if (alert):
					if self.pi:
						self.blink()
					else:
						time.sleep(LIGHT_RUN_TIME)

					remaining_time = t0 + ALERT_DISPLAY_TIME - time.time()
					if(remaining_time > 0):
						time.sleep(remaining_time)
				else:
					time.sleep(SLIDE_TIME)

				# All done!
				self.queue.task_done()
				self.logger.debug("Finished queue item. Queue size: %i" % self.queue.qsize())
			except Exception as e:
				self.logger.exception("Exception in printer: " + str(e))

