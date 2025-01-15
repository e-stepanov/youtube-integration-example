from dataclasses import dataclass
from functools import cached_property

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import Resource

from youtube.youtube_client import build_client


@dataclass
class YoutubeVideosApi:
    credentials: Credentials

    def list(self, video_ids: list[str]) -> dict:
        request = self.client.videos().list(
            part="snippet,contentDetails,status",
            id=",".join(video_ids),
        )
        return request.execute()

    @cached_property
    def client(self) -> Resource:
        return build_client(self.credentials)
