from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi
from restaurant_queries import get_restaurants

class webserverHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            if self.path.endswith("/restaurants"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                id_name = get_restaurants()
                output = ""
                output += "<html><body>"
                output += "<h1>Restaurants in the db</h1>"
                output += "<ul>"
                for (id, name) in id_name:
                    output += \
                    "<li>%s <a href=\"restaurant/%s/edit\">edit</a>\
                    <a href=\"confirm-delete\">delete</a> </li>" % \
                    (name, id)
                output += "</ul>"
                output += "</body></html>"
                self.wfile.write(output)
                return
            elif self.path.endswith("/restaurants/new"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "<h1>Add restaurant</h1>"
                output += """
                        <form action="cgi-bin/add_restaurant.cgi" method="post">
                            <label for="rest_name">Name:</label>
                            <input type="text" id="rest_name">
                            <input type="submit" value="submit">
                        </form>
                        """
                output += "</body></html>"
                self.wfile.write(output)
                return
            elif self.path.endswith("/edit"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write("edit")
                return
            elif self.path.endswith("/confirm-delete"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write("confirm-delete")
                return

        except IOError:
            self.send_error(404, "File Not Found %s" % self.path)

'''
    def do_POST(self):
        try:
            self.send_response(301)
            self.end_headers()
            ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
            if ctype == 'multipart/form-data':
                fields = cgi.parse_multipart(self.rfile, pdict)
                messagecontent = fields.get('message')
            output = ""
            output += "<html><body>"
            output += "<h2> Okay, how about this: </h2>"
            output += "<h1> %s </h1>" % messagecontent[0]
            output +=\
            """\
            <form method='POST'
                enctype='multipart/form-data'
                action='/hello'>
                <h2>What would you like me to say?</h2>
                <input name="message" type="text" ><input type="submit" value="Submit">
            </form>\
            """
            output += "</body></html>"
            self.wfile.write(output)
            print output
            return
        except:
            pass
'''


def main():
    try:
        port = 8080
        server = HTTPServer(('', port), webserverHandler)
        print "Web server running on port %s" % port
        server.serve_forever()
    except KeyboardInterrupt:
        print "^C entered, stopping web server ..."
        server.socket.close()

if __name__ == '__main__':
    main()
