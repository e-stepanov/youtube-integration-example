from datetime import datetime

from google.oauth2.credentials import Credentials
import pytest

pytest_plugins = [
    "app.testing.pytest_plugins",
]


@pytest.fixture
def gcloud_credentials() -> Credentials:
    return Credentials(
        token="token-test",
        refresh_token="refresh-test",
        client_id="google-client",
        client_secret="google-secret",
        scopes=["https://www.googleapis.com/auth/youtube.readonly"],
        token_uri="https://oauth2.googleapis.com/token",
        expiry=datetime(2030, 1, 1),
    )
