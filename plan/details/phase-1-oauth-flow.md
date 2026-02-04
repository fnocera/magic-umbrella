# Task 1.1: Implement OAuth 2.0 Authentication Flow

**Phase:** 1 - Authentication & Calendar Access
**Estimated Time:** 1 day
**Dependencies:** Task 0.2 (Azure app registration)

---

## Description

Implement the complete OAuth 2.0 Authorization Code Flow using MSAL (Microsoft Authentication Library) to authenticate users and obtain access tokens for Microsoft Graph API.

---

## Acceptance Criteria

### Authentication Module Created

- [x] `src/magic_umbrella/auth/authenticator.py` created ✅
- [x] `MicrosoftAuthenticator` class implemented ✅
- [x] OAuth 2.0 Authorization Code Flow working end-to-end ✅

### Core Functionality

- [x] Generate authorization URL with correct scopes ✅
- [x] Handle redirect callback and extract authorization code ✅
- [x] Exchange authorization code for access token ✅
- [x] Obtain refresh token for long-term access ✅
- [x] Implement token refresh mechanism ✅
- [x] Handle token expiration gracefully ✅

### User Experience

- [x] User redirected to Microsoft login page in browser ✅
- [x] After authentication, user redirected back to local app ✅
- [x] Success message displayed to user ✅
- [x] Access token obtained and ready for Graph API calls ✅

### Error Handling

- [x] Handle authentication cancellation ✅
- [x] Handle invalid authorization codes ✅
- [x] Handle network errors ✅
- [ ] Handle token refresh failures (basic handling, not comprehensive)
- [x] Provide clear error messages to user ✅

### Security

- [x] CSRF protection with `state` parameter ✅
- [x] Credentials loaded from environment variables (not hardcoded) ✅
- [ ] PKCE (Proof Key for Code Exchange) enabled if applicable (not needed for confidential client)
- [x] Scopes follow principle of least privilege ✅

---

## Implementation Details

### Class Structure

```python
# src/magic_umbrella/auth/authenticator.py

from msal import ConfidentialClientApplication
from typing import Optional, Dict
import webbrowser
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse

class MicrosoftAuthenticator:
    """Handles OAuth 2.0 authentication with Microsoft Identity Platform."""

    def __init__(
        self,
        client_id: str,
        client_secret: str,
        tenant_id: str,
        redirect_uri: str = "http://localhost:8000/callback",
        scopes: list[str] = None
    ):
        """Initialize authenticator with Azure app credentials."""
        pass

    def get_authorization_url(self) -> str:
        """Generate authorization URL for user to visit."""
        pass

    def authenticate_interactive(self) -> Dict[str, str]:
        """
        Perform interactive browser-based authentication.
        Returns dict with access_token and refresh_token.
        """
        pass

    def acquire_token_by_authorization_code(
        self,
        authorization_code: str
    ) -> Dict[str, str]:
        """Exchange authorization code for tokens."""
        pass

    def acquire_token_by_refresh_token(
        self,
        refresh_token: str
    ) -> Dict[str, str]:
        """Refresh access token using refresh token."""
        pass

    def is_token_valid(self, token: Dict[str, str]) -> bool:
        """Check if access token is still valid."""
        pass
```

### Required Configuration

Environment variables in `.env`:
```
AZURE_CLIENT_ID=your-client-id
AZURE_TENANT_ID=your-tenant-id
AZURE_CLIENT_SECRET=your-client-secret
AZURE_REDIRECT_URI=http://localhost:8000/callback
```

### Scopes to Request

```python
DEFAULT_SCOPES = [
    "https://graph.microsoft.com/Calendars.Read",
    "https://graph.microsoft.com/User.Read",
    "offline_access"  # For refresh token
]
```

### HTTP Server for Callback

Implement a simple HTTP server to handle the OAuth callback:
```python
class CallbackHandler(BaseHTTPRequestHandler):
    """Handle OAuth callback from Microsoft."""
    authorization_code = None

    def do_GET(self):
        """Handle GET request to callback URI."""
        # Parse authorization code from query string
        # Return success page to user
        # Store code for later exchange
        pass
```

---

## Testing Checklist

- [ ] Test successful authentication flow
- [ ] Test authentication cancellation
- [ ] Test invalid credentials
- [ ] Test token refresh
- [ ] Test with expired token
- [ ] Verify scopes are correctly requested
- [ ] Verify state parameter prevents CSRF

---

## References

- Research Document: [research/initial-research.md](../../research/initial-research.md) (Lines 123-229)
- OAuth Flow Diagram: [research/initial-research.md](../../research/initial-research.md) (Lines 140-178)
- MSAL Python: [research/initial-research.md](../../research/initial-research.md) (Lines 180-200)

---

## Validation Steps

1. Run authentication flow: `python -m magic_umbrella.auth.authenticator`
2. Browser opens to Microsoft login
3. Sign in with test account
4. Redirect back to localhost
5. Access token successfully obtained
6. Verify token can be used in Graph API call
