
import BaseHTTPServer
import SocketServer
class HTTPServer(SocketServer.ThreadingMixIn, BaseHTTPServer.HTTPServer):
	def __init__(self, server_address):
		SocketServer.TCPServer.__init__(self, server_address, HTTPHandler)

class HTTPHandler(BaseHTTPServer.BaseHTTPRequestHandler):
	"""
	HTTP Request Handler
	"""
	def do_GET(self): 
		if self.path == "/":
			response = """
			<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01//EN"
			"http://www.w3.org/TR/html4/strict.dtd">
			<html>
			<head>
			<title>Twitter Box</title>
			</head>
			<body>
			<h1>Hello from Twitter Box</h1>
			</body>
			</html>
			"""   
			self.send_response(200)
			self.send_header("Content-Length", str(len(response)))
			self.send_header("Cache-Control", "no-store")
			self.end_headers()
			self.wfile.write(response)

		elif self.path[:9] == "/JSStream":
			pass
		elif self.path[:10] == "/GetStream":
			pass
		else:
			self.send_error(404, "Banana Not Found.")
			self.end_headers()

	do_HEAD = do_POST = do_GET
	