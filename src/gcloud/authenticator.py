from functools import cached_property
import json

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

from app.cache import cache
from app import settings


CACHE_KEY = "youtube-api-credentials"


class GCloudAuthenticator:
    scopes = ["https://www.googleapis.com/auth/youtube.readonly"]

    def __call__(self) -> Credentials:
        if self.credentials_cache is None:
            return self.fetch()

        if self.credentials_cache.expired:
            refreshed = self.refresh_if_possible()
            if refreshed:
                return self.credentials_cache

        if not self.credentials_cache.valid:
            return self.fetch()

        return self.credentials_cache

    @cached_property
    def credentials_cache(self) -> Credentials | None:
        if CACHE_KEY in cache:
            return Credentials.from_authorized_user_info(
                json.loads(cache[CACHE_KEY]),
                self.scopes,
            )

    def fetch(self) -> Credentials:
        flow = InstalledAppFlow.from_client_config(
            settings.YOUTUBE_CREDENTIALS, self.scopes
        )
        credentials = flow.run_local_server(port=0)
        self.update_cache(credentials)

        return credentials

    def refresh_if_possible(self) -> bool:
        if self.credentials_cache is None or not self.credentials_cache.refresh_token:
            return False

        self.credentials_cache.refresh(Request())
        self.update_cache(self.credentials_cache)
        return True

    def update_cache(self, updated: Credentials) -> None:
        cache[CACHE_KEY] = updated.to_json()
