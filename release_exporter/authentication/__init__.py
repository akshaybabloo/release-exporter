import logging
from multiprocessing import Manager, Process
import sys
import time
import webbrowser

from flask import Flask


class AuthServerFlask:
    def __init__(self, host="127.0.0.1", port=8787):
        self.server_proc = None
        log = logging.getLogger("werkzeug")
        log.disabled = True
        cli = sys.modules["flask.cli"]
        cli.show_server_banner = lambda *x: None

        self.app = Flask(__name__)
        self.host = host
        self.port = port
        self.queue = Manager().Queue()

    def add_route(self, path, view_func):
        """Utility method to add routes to the Flask app from derived classes."""
        self.app.add_url_rule(path, view_func=view_func)

    def server_process(self):
        print("Starting Flask app in child process...")
        try:
            self.app.run(host=self.host, port=self.port, threaded=True)
        except Exception as e:
            print(f"Error in Flask app: {e}")

    def run(self):
        self.server_proc = Process(target=self.server_process)
        self.server_proc.start()
        time.sleep(1)

    @staticmethod
    def open_browser(path):
        print(f"If your browser doesn't open automatically, visit {path} to authenticate.")
        webbrowser.open(path)

    def shutdown_server(self):
        print(f"Attempting to shutdown server. Current state of self.server_proc: {self.server_proc}")
        if self.server_proc and self.server_proc.is_alive():
            self.server_proc.terminate()
            self.server_proc.join()
            print("Server process terminated.")
        else:
            print("Server process is not alive or _popen is None. It might have terminated prematurely.")
