from http.server import BaseHTTPRequestHandler, HTTPServer
import json


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


routes = []


class PyLogger():
    def __init__(self, file_name):
        self.__file_name = file_name + ".json"
        self.__result = None

        # Create file if it doesn't exist
        with open(self.file_name, "a") as file:
            pass

    @property
    def result(self):
        """
        Returns the result of the last read() call
        """
        return self.__result

    @property
    def file_name(self):
        """
        Returns the file name of the logger.
        """
        return self.__file_name

    def store(self, message):
        """
        Stores data in the log file, provided in the constructor of the `Logger` Object.
        """
        log_message = None
        try:
            log_message = json.loads(str(message))
        except Exception as err:
            PyHostr.error("Invalid JSON: " + str(err))
            return
        with open(self.file_name, "a") as file:
            file.write(json.dumps(log_message) + "\n")

    def read(self):
        with open(self.file_name, "r") as file:
            self.__result = json.loads(file.read())
            return self.result
    
    def clear(self):
        with open(self.file_name, "w") as file:
            file.truncate(0)


class PyHostr():
    def __init__(self, host, port):
        self.__host = host
        self.__port = port

    @property
    def host(self):
        return self.__host

    @property
    def port(self):
        return self.__port

    class Handler(BaseHTTPRequestHandler):

        def do_GET(self):
            print("Current path: " + self.path)
            # Handle GET requests, using objects in routes
            for obj in routes:
                if self.path == obj["route"] and str(obj["method"]).lower() == "get":
                    self.send_response(200)
                    # Send headers
                    for key, value in obj["response_headers"].items():
                        self.send_header(key, value)
                    self.end_headers()
                    self.wfile.write(
                        bytes(obj["response"], "utf8"))
                    return

            self.send_response(404)

        def do_OPTIONS(self):
            self.send_response(200, "ok")
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', '*')
            self.send_header("Access-Control-Allow-Headers", "*")
            self.send_header("Access-Control-Allow-Headers", "*")
            self.end_headers()

        def do_POST(self):
            for obj in routes:
                if self.path == obj["route"] and str(obj["method"]).lower() == "post":
                    self.send_response(200)
                    # Send headers
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.end_headers()
                    # Send custom reply and parse into JSON
                    data = self.rfile.read(
                        int(self.headers['Content-Length']))\
                        .decode("utf-8")\
                        .split("&")
                    result = {}
                    for arg in data:
                        temp = json.loads(arg)
                        for key, value in temp.items():
                            result[key] = str(value)
        
                    what_to_send = obj["handler"](result)
                    self.wfile.write(json.dumps(what_to_send).encode())

                    return

    def warn(self, message):
        print(bcolors.WARNING + "WARNING:\t" + message + bcolors.ENDC)

    def error(self, message):
        print(bcolors.FAIL + "ERROR:\t" + message + bcolors.ENDC)

    def success(self, message):
        print(bcolors.OKGREEN + "SUCCESS:\t" + message + bcolors.ENDC)

    def msg(self, message):
        print("MSG:\t" + message)

    def get(self, route, response="<h1>Default Response</h1>", response_headers={"Content-type": "text/html"}):
        # Add route to routes
        routes.append({
            "method": "GET",
            "route": route,
            # The HTML response
            "response": response,
            "response_headers": response_headers
        })

    def post(self, route, response_headers, handler):
        # Handle POST requests, using objects in routes
        routes.append({
            "method": "POST",
            "route": route,
            "response": response_headers,
            # Handler is a function that handles the POST request
            "handler": handler
        })

    def serve(self):
        # Start server
        server = HTTPServer((self.host, self.port), PyHostr.Handler)
        self.success("Server started http://%s:%s" %
                     (self.host, self.port))

        try:
            server.serve_forever()
        except KeyboardInterrupt:
            self.warn("\nStopping server...")
            self.success("Server stopped")
        server.server_close()
        print("Server stopped.")


# Showcase of PyHostr Usage

# This is a handler function which you specify when calling the post() method.
# NOTE: MAKE SURE TO NOT USE PARANTHESES WHEN PASSING THE FUNCTION TO THE post() METHOD

def parse_data(args):
    result = {}
    for arg in args:
        key, value = arg.split("=")
        result[key] = value
    return json.dumps(result)