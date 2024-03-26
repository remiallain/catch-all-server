import http.server
import socketserver
import os

class HttpRequestHandler(http.server.SimpleHTTPRequestHandler):
    def handle_one_request(self):
        try:
            # Reading the request line
            self.raw_requestline = self.rfile.readline(65537)
            self.requestline = ''
            self.request_version = ''
            self.command = ''
            self.server_version = os.environ.get("SERVER_NAME", "Dude, where's my server ?")
            self.sys_version = ''

            # Sending an '200 OK' response
            self.send_response(int(os.environ.get('STATUS_CODE', '200')))
            self.send_header("Content-type", os.environ.get("TYPE", "text/html"))
            self.end_headers()

            # Custom HTML code
            html = os.environ.get('CONTENT', '<h1>Not found</h1>')

            # Writing the HTML contents with UTF-8
            self.wfile.write(bytes(html, "utf8"))
            self.wfile.flush() #actually send the response if not already done.
        except Exception as e:
            self.close_connection = True
            return
            
server = socketserver.TCPServer(("", int(os.environ.get('PORT', "8000"))), HttpRequestHandler)

# Start the server
server.serve_forever()