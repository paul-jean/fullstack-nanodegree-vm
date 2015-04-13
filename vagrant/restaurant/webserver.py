from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi
import restaurant_queries
from restaurant_queries import get_restaurants, add_restaurant, \
        restaurant_exists, restaurant_name, change_name, delete_restaurant
import re
import logging

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
                output += "<h1>Create:</h1>"
                output += """<a href="restaurants/new">Create new restaurant</a>"""
                output += "<h1>Restaurants:</h1>"
                output += "<ul>"
                for (id, name) in id_name:
                    output += """
                    <li>%s
                        <a href="restaurant/%s/edit">edit</a>
                        <a href="restaurant/%s/delete">delete</a>
                    </li>
                    """ % (name, id, id)
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
                            <input type="submit" value="Submit">
                        </form>
                        """
                output += "</body></html>"
                self.wfile.write(output)
                return
            elif re.match("/restaurant/\d+/edit", self.path):
                id = re.search("/restaurant/(\d+)/edit", self.path).group(1)
                old_name = restaurant_name(id)
                output = ""
                output += "<html><body>"
                output += "<h1>%s</h1>" % old_name
                output += """
                        <form action="/restaurant/%s/edit"
                        enctype="multipart/form-data" method="post">
                            <input type="text" name="rest_name" placeholder="%s" >
                            <input type="submit" value="Rename">
                        </form>
                        """ % (id, old_name)
                output += "</body></html>"
                self.wfile.write(output)
            elif re.match("/restaurant/\d+/delete", self.path):
                id = re.search("/restaurant/(\d+)/delete", self.path).group(1)
                rest_name = restaurant_name(id)
                output = ""
                output += "<html><body>"
                output += "<h1>Are you sure you want to delete %s?</h1>" % rest_name
                output += """
                        <form action="/restaurant/%s/delete"
                        enctype="multipart/form-data" method="post">
                            <input type="submit" value="Delete">
                        </form>
                        """ % (id)
                output += "</body></html>"
                self.wfile.write(output)
        except IOError:
            self.send_error(404, "File Not Found %s" % self.path)

    def do_POST(self):
        try:
            if self.path.endswith("/restaurants/new"):
                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                rest_name = fields.get('rest_name')[0]
                exists = restaurant_exists(rest_name)
                add_result = ""
                if exists:
                    add_result += "<p>Restaurant %s already exists!</p>" % rest_name
                elif re.match("[A-Za-z0-9' ]+", rest_name) == None:
                    add_result += "<p>Restaurant name %s is not valid.</p>" % rest_name
                    add_result += "<p>Restaurant name can contain only alpha-numeric\
                            characters: [A-Za-z0-9' ]+</p>"
                else:
                    add_restaurant(rest_name)
                self.send_response(301)
                # send redirect back to /restaurants:
                self.send_header('Content-type', 'text/html')
                self.send_header('Location', '/restaurants')
                self.end_headers()
                return
            elif re.match(".*?/restaurant/\d+/edit", self.path):
                id = re.search(".*?/restaurant/(\d+)/edit", self.path).group(1)
                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                new_name = fields.get('rest_name')[0]
                change_name(id, new_name)
                self.send_response(301)
                # send redirect back to /restaurants:
                self.send_header('Content-type', 'text/html')
                self.send_header('Location', '/restaurants')
                self.end_headers()
                return
            elif re.match(".*?/restaurant/\d+/delete", self.path):
                id = re.search(".*?/restaurant/(\d+)/delete", self.path).group(1)
                delete_restaurant(id)
                self.send_response(301)
                # send redirect back to /restaurants:
                self.send_header('Content-type', 'text/html')
                self.send_header('Location', '/restaurants')
                self.end_headers()
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
