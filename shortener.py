#!/usr/bin/python3

# Adrián Montes Linares

from webapp import webApp
from urllib import parse
import random
import string
import shelve

PAGE = """
<html>
    <body>
        {content}
        <hr>
        {form}
        <hr>
        <h3>{urls}</h3>
    </body>
</html>
"""


ERROR_NOT_FOUND = """
<html>
    <body>
        <h1>Error 404</h1>
        Error 404 NOT FOUND: {resource}
        </hr1>
    </body>
</html>
"""


FORM = """
<form action='/' method="post">
    <div>
        <label>Resorce name: </label>
        <input type="text" name="url" required>
    </div>
    <div>
        <input type="submit" value="SEND">
    </div>

</form>
"""

NOT_ALLOWED = """
<html>
    <body>
        Method not found: {resource}
    </body>
</html>
"""

DEFAULT_CONTENTS = {
            '/': "<p>MAIN PAGE<p>"
        }


class Shortener(webApp):

    # Ranges for the short url, between 5-10
    MIN_RANGE = 5
    MAX_RANGE = 10

    contents = None

    def parse(self, request):
        # Get the name of the resoruce
        data = {}
        body_start = request.find("\r\n\r\n")

        if body_start == -1:
            data['body'] = None
        else:
            # Adjusted to skip "\r\n\r\n"
            data['body'] = request[body_start + 4:]

        parts = request.split(' ', 2)
        try:
            print(f"PARTS: {parts}")
            data['method'] = parts[0]
            data['resource'] = parts[1]
        except IndexError:
            # To avoid the server close with and error
            # default put the values of the main page
            data['method'] = "GET"
            data['resource'] = "/"
        return data

    def show_main_page(self, contenido):
        # Create all the main page
        page = "<ul>"
        for short, url in self.contents.items():
            if short != "/":
                page += f"<li>{short} - {url}</li>"
        page += "</ul>"
        html_pagina = PAGE.format(content=contenido, form=FORM, urls=page)
        http_code = "200 OK"
        return http_code, html_pagina

    def check_if_contents(self, request_resource):
        # Check if its in contents request_resource
        return request_resource in self.contents

    def its_main_page(self, request_resource):
        # Check if its a / the request_resource
        return request_resource == "/"

    def show_the_resource(self, request_resource):
        # Shearch the request_resource in our contents
        # and then redirect to that page
        for short_url in self.contents.keys():
            if short_url == request_resource:
                # Move the user to the resource he/she ask
                print(f"Redirigiendo a {self.contents[short_url]}")
                code = "301 Moved Permanently"
                http_code = f"{code}\r\nLocation:{self.contents[short_url]}"
                html_pagina = "<html></html>"
                break
        return http_code, html_pagina

    def get(self, rq_source):
        # Default 404 not found
        http_code = "404 Not Found"
        html_pagina = ERROR_NOT_FOUND.format(resource=rq_source)

        # Check if request_resource its in contents
        if self.check_if_contents(rq_source):
            # The content its the value of the key in request_resource
            contenido = self.contents[rq_source]
            if self.its_main_page(rq_source):
                # Show the main page to the user
                http_code, html_pagina = self.show_main_page(contenido)
            else:
                # Redirect the user to the page he/she ask
                http_code, html_pagina = self.show_the_resource(rq_source)

        return http_code, html_pagina

    def generate_short_url(self):
        # Generate the shor url
        longitud = random.randint(self.MIN_RANGE, self.MAX_RANGE)
        caracteres = string.ascii_letters + string.digits
        return ''.join(random.choice(caracteres) for i in range(longitud))

    def extract_url(self, url):
        # Get the url and manage if start cott
        if not (url.startswith("http://") or url.startswith("https://")):
            url = "https://" + url
        if not (url.endswith(".com") or url.endswith(".es")):
            url = url + ".com"
        return url

    def its_saved_url(self, url):
        # Check if the url its on the server
        return url not in self.contents.values()

    def post(self, body):
        # Generate new resource
        field = parse.parse_qs(body)
        url = self.extract_url(field["url"][0])

        # If the url its not on the server
        # generate short url and save in contents
        if self.its_saved_url(url):
            url_short = self.generate_short_url()
            self.contents["/" + url_short] = url

        # Now redirect to http://localhost:1234
        http_code = f"301 Moved Permanently\r\nLocation: http://localhost:1234"
        html_page = "<html></html>"
        return http_code, html_page + html_page

    def save_urls(self):
        # Save contents in urls_saved
        with shelve.open('urls_saved') as archivo_shelve:
            archivo_shelve['contents'] = self.contents

    def open_urls(self):
        # Try to open urls_saved
        # if not exits or error self.contets get the DEFAULT values
        try:
            with shelve.open('urls_saved') as save:
                # Get the contents of urls_saved
                self.contents = save['contents']
        except KeyError:
            # Asign DEFAULT_CONTENTS to self.contents
            self.contents = DEFAULT_CONTENTS

    def manage_wrong_method(self, body):
        # If wrong method, manage
        http_code = "405 METHOD NOT ALLOWED"
        html_page = NOT_ALLOWED.format(resource=body)

        return http_code, html_page

    def procces(self, rq_data):
        # Procces new resource for the response
        # Default values for http_code and html_page
        http_code, html_page = None, None

        # Open the urls saved
        self.open_urls()

        # Manage GET POST and wrong method
        if rq_data['method'] == 'GET':
            http_code, html_page = self.get(rq_data['resource'])
        elif rq_data['method'] == 'POST':
            http_code, html_page = self.post(rq_data['body'])
        else:
            http_code, html_page = self.manage_wrong_method(rq_data['body'])

        # Save the urls
        self.save_urls()

        return http_code, html_page


if __name__ == '__main__':
    try:
        app = Shortener('', 1234)
    except KeyboardInterrupt:
        print("\n\nClosing the server...\n\n")
