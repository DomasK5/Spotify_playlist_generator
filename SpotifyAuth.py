import base64
import json
import random
import webbrowser
from requests import post, get
import urllib.parse
import http.server
import socketserver
import threading
import secret1


class SpotifyAuth:
    """Class for handling Spotify authentication and token management"""

    def __init__(self):
        self.client_id = secret1.CLIENT_ID
        self.client_secret = secret1.CLIENT_SECRET
        self.redirect_uri = secret1.REDIRECT_URI
        self.token = None
        self.refresh_token = None
        self.auth_code = None
        self.user_id = None
        self.access_token = None
        self.auth_completed = False
        self.auth_event = threading.Event()

    def get_token(self):
        """Obtain a Spotify API token using client credentials flow"""
        auth_string = self.client_id + ":" + self.client_secret
        auth_bytes = auth_string.encode('utf-8')
        auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

        url = "https://accounts.spotify.com/api/token"
        headers = {
            "Authorization": "Basic " + auth_base64,
            "Content-Type": "application/x-www-form-urlencoded"
        }
        data = {"grant_type": "client_credentials"}

        result = post(url, headers=headers, data=data)
        json_result = json.loads(result.content)

        if "access_token" in json_result:
            self.token = json_result["access_token"]
            return self.token
        else:
            print(f"Error getting token: {json_result}")
            return None

    def get_auth_header(self):
        """Return the authorization header with token"""
        if not self.token:
            self.get_token()
        return {"Authorization": "Bearer " + self.token}

    def start_auth_server(self):
        """Start local server to handle OAuth callback"""
        auth_self = self

        class AuthHandler(http.server.BaseHTTPRequestHandler):
            def do_GET(self):
                query_components = urllib.parse.parse_qs(
                    urllib.parse.urlparse(self.path).query)

                if 'code' in query_components:
                    auth_code = query_components['code'][0]
                    auth_self.auth_code = auth_code

                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()

                    response_content = """
                    <html>
                    <head>
                        <title>Authentication Successful</title>
                        <style>
                            body { font-family: Arial, sans-serif; text-align: center; padding-top: 50px; }
                            h1 { color: #1DB954; }
                            p { margin: 20px 0; }
                        </style>
                    </head>
                    <body>
                        <h1>Authentication Successful!</h1>
                        <p>You can now close this window and return to the application.</p>
                        <script>
                            setTimeout(function() {
                                window.close();
                            }, 3000);
                        </script>
                    </body>
                    </html>
                    """
                    self.wfile.write(response_content.encode('utf-8'))

                    auth_self.process_auth_code()
                    auth_self.auth_completed = True
                    auth_self.auth_event.set()
                else:
                    self.send_response(400)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()

                    error_content = """
                    <html>
                    <head>
                        <title>Authentication Failed</title>
                        <style>
                            body { font-family: Arial, sans-serif; text-align: center; padding-top: 50px; }
                            h1 { color: #FF0000; }
                            p { margin: 20px 0; }
                        </style>
                    </head>
                    <body>
                        <h1>Authentication Failed</h1>
                        <p>Please try again from the application.</p>
                    </body>
                    </html>
                    """
                    self.wfile.write(error_content.encode('utf-8'))

            def log_message(self, format, *args):
                return

        parsed_uri = urllib.parse.urlparse(self.redirect_uri)
        port = parsed_uri.port or 8888

        server = socketserver.TCPServer(('localhost', port), AuthHandler)
        server_thread = threading.Thread(target=server.serve_forever)
        server_thread.daemon = True
        server_thread.start()

        self.server = server
        self.server_thread = server_thread

        return server

    def process_auth_code(self):
        """Exchange authorization code for access token"""
        if not self.auth_code:
            print("No authorization code available")
            return False

        url = "https://accounts.spotify.com/api/token"

        payload = {
            "grant_type": "authorization_code",
            "code": self.auth_code,
            "redirect_uri": self.redirect_uri,
            "client_id": self.client_id,
            "client_secret": self.client_secret
        }

        response = post(url, data=payload)

        if response.status_code == 200:
            token_data = json.loads(response.content)
            self.access_token = token_data.get("access_token")
            self.refresh_token = token_data.get("refresh_token")

            if self.access_token:
                self.get_user_profile()

            return True
        else:
            print(f"Error exchanging code for token: {response.content}")
            return False

    def get_user_profile(self):
        """Get user's Spotify profile to get user ID"""
        if not self.access_token:
            print("No access token available")
            return False

        headers = {"Authorization": f"Bearer {self.access_token}"}
        response = get("https://api.spotify.com/v1/me", headers=headers)

        if response.status_code == 200:
            user_data = json.loads(response.content)
            self.user_id = user_data.get("id")
            return True
        else:
            print(f"Error getting user profile: {response.content}")
            return False

    def open_auth_page(self):
        """Start the authorization process"""
        self.auth_code = None
        self.access_token = None
        self.user_id = None
        self.auth_completed = False
        self.auth_event.clear()

        self.start_auth_server()

        state = str(random.randint(10000, 99999))

        auth_params = {
            "client_id": self.client_id,
            "response_type": "code",
            "redirect_uri": self.redirect_uri,
            "scope": "playlist-modify-public playlist-modify-private user-read-private",
            "state": state
        }

        auth_url = "https://accounts.spotify.com/authorize?" + urllib.parse.urlencode(auth_params)

        webbrowser.open(auth_url)

        return True

    def wait_for_auth_completion(self, timeout=120):
        """Wait for authentication to complete with timeout"""
        return self.auth_event.wait(timeout)

    def shutdown_server(self):
        """Shutdown the local server"""
        if hasattr(self, 'server') and self.server:
            self.server.shutdown()
            self.server.server_close()
