import threading
import settings
import cherrypy


class HelloWorld:
	def __init__(self, queue):
		self.queue = queue

	def index(self):
		return "Hello world! queue size is %i" % self.queue.qsize()
	index.exposed = True

	def trigger(self):
		self.queue.put((settings.PRIORITY_HIGH, "@fakeuser" + ":", "Check it out dudes! I totally tweeted!", True))
	trigger.exposed = True	
	
class Server(threading.Thread):
	def __init__(self, queue, logger):
		threading.Thread.__init__(self)
		self.queue = queue
		self.logger = logger
		self.logger.debug("Server created")

	def run(self):
		try:
			cherrypy.quickstart(HelloWorld(self.queue))
		except Exception as e:
			self.logger.exception("Exception in server: " + str(e))
