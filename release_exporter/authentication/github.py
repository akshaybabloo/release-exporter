import base64
import json
import threading
import time
from uuid import uuid4

from flask import request
from yarl import URL

from release_exporter.authentication import AuthServerFlask


class GithubAuthenticator(AuthServerFlask):
    def __init__(self, host="127.0.0.1", port=8787):
        super().__init__(host, port)

        self.add_route("/token", self.token_handler)
        self.add_route("/done", self.done_handler)

    def token_handler(self):
        """
        This method is called when the user has authenticated and the token is received.
        """
        self.token = token

    def done_handler(self):
        """
        This method is called when the user has authenticated and the token is received.
        """
        token = request.args.get("token", "")
        if not token:
            return "No token received", 400

        self.queue.put(token)
        return "Done!"

    def run(self):
        state = {"redirect_uri": f"http://{self.host}:{self.port}/token", "uuid": str(uuid4())}

        queries = {"state": base64.b64encode(json.dumps(state).encode("utf-8")).decode(), "scope": "repo user"}
        api_url = URL.build(scheme="https", host="rex.gollahalli.com", path="/api/github/auth", query=queries)

        self.open_browser(str(api_url))
        super().run()


if __name__ == "__main__":
    auth = GithubAuthenticator()
    auth.run()

    try:
        token = auth.queue.get()
        print(f"Received token: {token}")

        # Delay shutdown in a background thread so response can complete
        def delayed_shutdown():
            time.sleep(1)  # Let response finish sending
            auth.shutdown_server()

        threading.Thread(target=delayed_shutdown, daemon=True).start()
    except Exception as e:
        print(f"Error receiving token: {e}")
        exit(1)
