import pytest

from youtube.youtube_videos_api import YoutubeVideosApi

pytestmark = [
    pytest.mark.httpretty,
]


@pytest.fixture()
def get_list(gcloud_credentials):
    return lambda: YoutubeVideosApi(credentials=gcloud_credentials).list(["1"])


def test_list_result_is_returned(get_list, youtube_videos_list_api_response):
    result = get_list()

    assert result == youtube_videos_list_api_response
