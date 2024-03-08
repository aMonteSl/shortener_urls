# URL Shortener Web Application

This Python script implements a simple URL shortener web application. It allows users to shorten long URLs into shorter ones, making them easier to share or remember.

## How It Works

The URL shortener works by mapping a user-provided long URL to a randomly generated short code. This short code is appended to the base URL of the web application, allowing users to access the original URL through the shortened link.

### Features

- Shorten long URLs into shorter ones.
- Redirect users from the shortened URL to the original long URL.
- Display a main page listing all the shortened URLs along with their corresponding original URLs.
- Saving URLs persistently using the `shelve` module.
- Handling HTTP GET and POST requests appropriately.
- Error handling mechanisms for common scenarios.
- URL validation and manipulation to ensure proper formatting.
- Random short URL generation for uniqueness and security.
- Command-line interface for easy execution and server management.

## Usage

### Running the Application

To run the URL shortener web application, execute the provided Python script `shortener.py`:

```bash
python3 shortener.py
```

Or

```bash
chmod +x shortener.py
./shortener.py
```


By default, the web application will listen on port `1234`.

### Accessing the Application

Once the application is running, you can access it through a web browser or by sending HTTP requests to `http://localhost:1234`.

### Shortening a URL

To shorten a URL, navigate to the main page of the web application. Enter the long URL into the provided form and submit it. The web application will generate a shortened URL for you.

### Accessing Shortened URLs

You can access the shortened URLs directly in your web browser or by sending HTTP GET requests to the generated URLs. The web application will redirect you to the original long URL associated with the shortened link.

## Additional Functions

In addition to URL shortening and redirection, the URL shortener web application includes the following functions:

### Saving URLs

The application saves the mappings between shortened URLs and original long URLs persistently using the `shelve` module. This ensures that the mappings are retained even after the application is restarted.

```python
def save_urls(self):
    # Save contents in urls_saved
    with shelve.open('urls_saved') as archivo_shelve:
        archivo_shelve['contents'] = self.contents
```

### Handling HTTP Methods

The application handles HTTP GET and POST requests appropriately. GET requests are used to retrieve and display web pages, while POST requests are used to submit data to be processed by the server, such as shortening a URL.

```python
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
```

### Error Handling

The application includes error handling mechanisms to handle various scenarios, such as:

    404 Not Found: When the requested resource is not found.
    405 Method Not Allowed: When an unsupported HTTP method is used.

```python
ERROR_NOT_FOUND = """
<html>
    <body>
        <h1>Error 404</h1>
        Error 404 NOT FOUND: {resource}
        </hr1>
    </body>
</html>
"""
NOT_ALLOWED = """
<html>
    <body>
        Method not found: {resource}
    </body>
</html>
"""
```

### Main Page Display

The main page of the web application displays a list of all the shortened URLs along with their corresponding original URLs. This allows users to easily manage and access their shortened links

```python
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
```

### URL Validation and Manipulation

Before shortening a URL, the application validates and manipulates the input URL to ensure it is properly formatted and includes the necessary components (e.g., protocol, domain).

```python
def extract_url(self, url):
    # Get the url and manage if start cott
    if not (url.startswith("http://") or url.startswith("https://")):
        url = "https://" + url
    if not (url.endswith(".com") or url.endswith(".es")):
        url = url + ".com"
    return url
```

### Random Short URL Generation

The application generates random short codes for shortened URLs to ensure uniqueness and security. These short codes consist of a combination of letters and digits within a specified length range.


```python
def generate_short_url(self):
    # Generate the shor url
    longitud = random.randint(5, 10)
    caracteres = string.ascii_letters + string.digits
    return ''.join(random.choice(caracteres) for i in range(longitud))
```

### Command-Line Interface

The application can be executed from the command line, allowing users to easily start and stop the web server. Additionally, it provides feedback to the user, such as notifying when the server is being closed due to a keyboard interrupt (e.g., Ctrl+C).

```python
if __name__ == '__main__':
    try:
        app = Shortener('', 1234)
    except KeyboardInterrupt:
        print("\n\nClosing the server...\n\n")
```

### Dependencies

The following dependencies are required to run the web application:

1. Python 3
2. webapp module (Assumed to be provided separately)
