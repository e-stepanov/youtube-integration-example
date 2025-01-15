from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build as build_resource
from googleapiclient.discovery import Resource


def build_client(credentials: Credentials) -> Resource:
    return build_resource(
        "youtube",
        "v3",
        credentials=credentials,
        cache_discovery=False,
    )
