import threading
import settings
from cherrypy import *
import os
from mako.template import Template
from mako.lookup import TemplateLookup
lookup = TemplateLookup(directories=['template'])

config.update({'server.socket_host': '0.0.0.0',
						'server.socket_port': settings.SERVER_PORT,
					   })

class HelloWorld:
	def __init__(self, queue):
		self.queue = queue

	def index(self):
		tmpl = lookup.get_template("index.html")
		return tmpl.render(size=self.queue.qsize())
	index.exposed = True

	def trigger(self):
		if request.method == 'POST':
			self.queue.put((settings.PRIORITY_HIGH, settings.FAKE_TWEET, "", True))
		raise HTTPRedirect('/')
	trigger.exposed = True	
	
class Server(threading.Thread):
	def __init__(self, queue, logger):
		threading.Thread.__init__(self)
		self.queue = queue
		self.logger = logger
		self.logger.debug("Server created")

	def run(self):
		try:
			this_dir = os.path.abspath(os.path.join(__file__, '..'))
			conf = {'/':
				{
					'tools.staticdir.root': this_dir,
					'tools.staticdir.on': True,
					'tools.staticdir.dir': "static",
					'tools.mako.directories': os.path.join(this_dir, 'template')
				}
			}
			tree.mount(HelloWorld(self.queue), '/', conf)
			engine.start()
			engine.block()
		except Exception as e:
			self.logger.exception("Exception in server: " + str(e))
