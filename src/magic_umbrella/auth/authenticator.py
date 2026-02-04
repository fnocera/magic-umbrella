"""OAuth 2.0 authentication with Microsoft Identity Platform using MSAL."""

import os
import secrets
import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer
from threading import Thread
from typing import Optional
from urllib.parse import parse_qs, urlparse

from dotenv import load_dotenv
from msal import ConfidentialClientApplication

# Load environment variables
load_dotenv()

# Default scopes for Microsoft Graph API
DEFAULT_SCOPES = [
    "https://graph.microsoft.com/Calendars.Read",
    "https://graph.microsoft.com/User.Read",
]


class CallbackHandler(BaseHTTPRequestHandler):
    """Handle OAuth callback from Microsoft Identity Platform."""

    authorization_code: Optional[str] = None
    error: Optional[str] = None
    state: Optional[str] = None

    def do_GET(self):
        """Handle GET request to callback URI."""
        # Parse query parameters
        parsed_url = urlparse(self.path)
        params = parse_qs(parsed_url.query)

        # Extract authorization code or error
        if "code" in params:
            CallbackHandler.authorization_code = params["code"][0]
            CallbackHandler.state = params.get("state", [None])[0]

            # Send success response to browser
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            success_html = """
            <!DOCTYPE html>
            <html>
            <head><title>Authentication Successful</title></head>
            <body style="font-family: Arial; text-align: center; padding: 50px;">
                <h1 style="color: green;">✓ Authentication Successful!</h1>
                <p>You can close this window and return to the application.</p>
            </body>
            </html>
            """
            self.wfile.write(success_html.encode())

        elif "error" in params:
            CallbackHandler.error = params["error"][0]
            error_description = params.get("error_description", ["Unknown error"])[0]

            # Send error response to browser
            self.send_response(400)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            error_html = f"""
            <!DOCTYPE html>
            <html>
            <head><title>Authentication Failed</title></head>
            <body style="font-family: Arial; text-align: center; padding: 50px;">
                <h1 style="color: red;">✗ Authentication Failed</h1>
                <p>{error_description}</p>
                <p>You can close this window and try again.</p>
            </body>
            </html>
            """
            self.wfile.write(error_html.encode())

    def log_message(self, format, *args):
        """Suppress HTTP server log messages."""
        pass


class MicrosoftAuthenticator:
    """Handles OAuth 2.0 authentication with Microsoft Identity Platform."""

    def __init__(
        self,
        client_id: Optional[str] = None,
        client_secret: Optional[str] = None,
        tenant_id: Optional[str] = None,
        redirect_uri: str = "http://localhost:8000/callback",
        scopes: Optional[list[str]] = None,
    ):
        """Initialize authenticator with Azure app credentials.

        Args:
            client_id: Azure app client ID (or from AZURE_CLIENT_ID env var)
            client_secret: Azure app client secret (or from AZURE_CLIENT_SECRET env var)
            tenant_id: Azure tenant ID (or from AZURE_TENANT_ID env var)
            redirect_uri: OAuth redirect URI (default: http://localhost:8000/callback)
            scopes: List of Microsoft Graph scopes (default: DEFAULT_SCOPES)
        """
        self.client_id = client_id or os.getenv("AZURE_CLIENT_ID")
        self.client_secret = client_secret or os.getenv("AZURE_CLIENT_SECRET")
        self.tenant_id = tenant_id or os.getenv("AZURE_TENANT_ID")
        self.redirect_uri = redirect_uri
        self.scopes = scopes or DEFAULT_SCOPES

        # Validate required credentials
        if not all([self.client_id, self.client_secret, self.tenant_id]):
            raise ValueError(
                "Missing required credentials. Set AZURE_CLIENT_ID, "
                "AZURE_CLIENT_SECRET, and AZURE_TENANT_ID environment variables."
            )

        # Initialize MSAL app
        authority = f"https://login.microsoftonline.com/{self.tenant_id}"
        self.app = ConfidentialClientApplication(
            client_id=self.client_id,
            client_credential=self.client_secret,
            authority=authority,
        )

        # State parameter for CSRF protection
        self.state = None

    def get_authorization_url(self) -> str:
        """Generate authorization URL for user to visit.

        Returns:
            Authorization URL string
        """
        # Generate random state for CSRF protection
        self.state = secrets.token_urlsafe(32)

        # Build authorization URL with account selection prompt
        auth_url = self.app.get_authorization_request_url(
            scopes=self.scopes,
            state=self.state,
            redirect_uri=self.redirect_uri,
            prompt="select_account",  # Force account selection
        )

        return auth_url

    def authenticate_interactive(self) -> dict[str, str]:
        """Perform interactive browser-based authentication.

        Returns:
            Dictionary containing access_token, refresh_token, and other token info

        Raises:
            RuntimeError: If authentication fails
        """
        # Reset callback handler state
        CallbackHandler.authorization_code = None
        CallbackHandler.error = None
        CallbackHandler.state = None

        # Get authorization URL
        auth_url = self.get_authorization_url()

        # Start local HTTP server for callback
        server_address = ("", 8000)
        httpd = HTTPServer(server_address, CallbackHandler)

        # Run server in background thread
        server_thread = Thread(target=self._run_callback_server, args=(httpd,), daemon=True)
        server_thread.start()

        # Open browser for user to authenticate
        print("Opening browser for authentication...")
        print(f"If browser doesn't open automatically, visit: {auth_url}")
        webbrowser.open(auth_url)

        # Wait for callback (server will shut down after receiving callback)
        server_thread.join(timeout=300)  # 5 minute timeout

        # Check for errors
        if CallbackHandler.error:
            raise RuntimeError(f"Authentication failed: {CallbackHandler.error}")

        if not CallbackHandler.authorization_code:
            raise RuntimeError("Authentication timed out or was cancelled")

        # Verify state parameter (CSRF protection)
        if CallbackHandler.state != self.state:
            raise RuntimeError("State mismatch - possible CSRF attack detected")

        # Exchange authorization code for tokens
        result = self.acquire_token_by_authorization_code(CallbackHandler.authorization_code)

        print("✓ Authentication successful!")
        return result

    def _run_callback_server(self, httpd: HTTPServer):
        """Run HTTP server to handle OAuth callback.

        Args:
            httpd: HTTPServer instance
        """
        # Handle single request (the callback)
        httpd.handle_request()
        httpd.server_close()

    def acquire_token_by_authorization_code(self, authorization_code: str) -> dict[str, str]:
        """Exchange authorization code for access and refresh tokens.

        Args:
            authorization_code: Authorization code from OAuth callback

        Returns:
            Dictionary containing access_token, refresh_token, and other token info

        Raises:
            RuntimeError: If token acquisition fails
        """
        result = self.app.acquire_token_by_authorization_code(
            code=authorization_code, scopes=self.scopes, redirect_uri=self.redirect_uri
        )

        if "error" in result:
            error_desc = result.get("error_description", result["error"])
            raise RuntimeError(f"Failed to acquire token: {error_desc}")

        return result

    def acquire_token_by_refresh_token(self, refresh_token: str) -> dict[str, str]:
        """Refresh access token using refresh token.

        Args:
            refresh_token: Refresh token from previous authentication

        Returns:
            Dictionary containing new access_token and other token info

        Raises:
            RuntimeError: If token refresh fails
        """
        # MSAL handles refresh tokens internally via acquire_token_silent
        # But we can also manually refresh if needed
        accounts = self.app.get_accounts()

        if not accounts:
            raise RuntimeError("No accounts found. Please re-authenticate.")

        # Try to get token silently (uses refresh token automatically)
        result = self.app.acquire_token_silent(scopes=self.scopes, account=accounts[0])

        if not result:
            raise RuntimeError("Failed to refresh token. Please re-authenticate.")

        if "error" in result:
            error_desc = result.get("error_description", result["error"])
            raise RuntimeError(f"Failed to refresh token: {error_desc}")

        return result

    def is_token_valid(self, token: dict[str, str]) -> bool:
        """Check if access token is still valid.

        Args:
            token: Token dictionary containing 'expires_in' or 'expires_at'

        Returns:
            True if token is valid, False otherwise
        """
        # MSAL handles token expiration automatically
        # This is a utility method for explicit checks
        if "expires_in" in token:
            return token["expires_in"] > 60  # Buffer of 60 seconds

        # If using token cache, MSAL will handle expiration
        return True


# Utility function for quick authentication
def authenticate() -> dict[str, str]:
    """Quick authentication helper function.

    Returns:
        Dictionary containing access_token and other token info
    """
    authenticator = MicrosoftAuthenticator()
    return authenticator.authenticate_interactive()


# Allow running module directly for testing
if __name__ == "__main__":
    print("=== Magic Umbrella - Authentication Test ===")
    print()

    try:
        token_data = authenticate()
        print()
        print("Token acquired successfully!")
        print(f"Access token: {token_data['access_token'][:50]}...")
        print(f"Expires in: {token_data.get('expires_in', 'N/A')} seconds")
        print(f"Scopes: {token_data.get('scope', 'N/A')}")

    except Exception as e:
        print(f"❌ Authentication failed: {e}")
        exit(1)
