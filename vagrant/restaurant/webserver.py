from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi
import restaurant_queries
from restaurant_queries import get_restaurants, add_restaurant, \
        restaurant_exists

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
                print "restaurants/new"
                output = ""
                output += "<html><body>"
                output += "<h1>Add restaurant</h1>"
                output += """
                        <form action=""
                        enctype="multipart/form-data" method="post">
                            <label for="rest_name">Name:</label>
                            <input type="text" name="rest_name">
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

    def do_POST(self):
        try:
            self.send_response(301)
            self.end_headers()
            ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
            if ctype == 'multipart/form-data':
                fields = cgi.parse_multipart(self.rfile, pdict)
            rest_name = fields.get('rest_name')[0]
            print "rest_name:"
            print rest_name
            exists = restaurant_exists(rest_name)
            print "exists:"
            print exists
            add_result = ""
            if exists:
                add_result += "<p>Restaurant %s already exists!</p>" % rest_name
                print add_result
            elif re.match("[A-Za-z0-9' ]+", rest_name) == None:
                add_result += "<p>Restaurant name %s is not valid.</p>" % rest_name
                add_result += "<p>Restaurant name can contain only alpha-numeric\
                        characters: [A-Za-z0-9' ]+</p>"
                print add_result
            else:
                add_result += "<p>Adding restaurant %s ...</p>" % rest_name
                print add_result
                add_restaurant(rest_name)
            print "add_result:"
            print add_result
            output = ""
            output += "<html><body>"
            output += add_result
            output += "<h1>Add restaurant</h1>"
            output += """
                    <form action="/restaurants/new"
                    enctype="multipart/form-data" method="post">
                        <label for="rest_name">Name:</label>
                        <input type="text" id="rest_name">
                        <input type="submit" value="submit">
                    </form>
                    """
            output += "</body></html>"
            self.wfile.write(output)
            print output
            return
        except:
            pass


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
