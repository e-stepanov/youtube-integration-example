import json
import httpretty

import pytest


@pytest.fixture
def youtube_videos_list_api_response() -> dict:
    return {
        "kind": "youtube#videoListResponse",
        "etag": "etag",
        "nextPageToken": "next-page-token",
        "prevPageToken": "prev-page-token",
        "pageInfo": {"totalResults": "1", "resultsPerPage": "50"},
        "items": [
            {
                "kind": "youtube#video",
                "etag": "etag",
                "id": "youtube-video-0",
                "snippet": {
                    "publishedAt": "2020-03-01T12:10:00Z",
                    "channelId": "channel-id-0",
                    "title": "Почему не работает",
                    "description": "Пишем автотесты",
                    "channelTitle": "Тыжпрограммист",
                },
                "contentDetails": {
                    "duration": "100",
                },
                "status": {
                    "privacyStatus": "public",
                },
            }
        ],
    }


@pytest.fixture(autouse=True)
def _youtube_videos_list_api_mock(youtube_videos_list_api_response: dict) -> None:
    httpretty.register_uri(
        httpretty.GET,
        "https://youtube.googleapis.com/youtube/v3/videos",
        body=json.dumps(youtube_videos_list_api_response),
    )
