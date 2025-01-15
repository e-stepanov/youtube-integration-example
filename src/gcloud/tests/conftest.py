import pytest

from app.cache import cache


@pytest.fixture
def app_cache():
    yield cache
    cache.clear()


@pytest.fixture
def credentials_cache(gcloud_credentials, app_cache):
    credentials_cache = gcloud_credentials.to_json()
    app_cache["youtube-api-credentials"] = credentials_cache
    return credentials_cache
