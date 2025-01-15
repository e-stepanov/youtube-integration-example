from datetime import datetime
import json
import pytest

from google.oauth2.credentials import Credentials

from gcloud.authenticator import GCloudAuthenticator


@pytest.fixture(autouse=True)
def run_local_server_mock(mocker, gcloud_credentials):
    return mocker.patch(
        "google_auth_oauthlib.flow.InstalledAppFlow.run_local_server",
        return_value=gcloud_credentials,
    )


@pytest.fixture()
def refresh_credentials_mock(mocker):
    return mocker.patch(
        "google.oauth2.reauth.refresh_grant",
        return_value=(
            "updated-access-token",
            "updated-refresh-token",
            datetime(2031, 1, 1),
            {},
            "rapt-token",
        ),
    )


@pytest.fixture()
def authenticator():
    return GCloudAuthenticator()


def test_fetching_new_credentials(
    authenticator,
    run_local_server_mock,
    gcloud_credentials,
):
    fetched_credentials = authenticator()

    run_local_server_mock.assert_called_once()
    assert fetched_credentials == gcloud_credentials


def test_saving_new_credentials(app_cache, authenticator, gcloud_credentials):
    authenticator()

    credentials = app_cache["youtube-api-credentials"]
    assert json.loads(credentials) == json.loads(gcloud_credentials.to_json())


def test_override_invalid_credentials_cache(
    mocker,
    app_cache,
    authenticator,
    gcloud_credentials,
):
    old_credentials = json.loads(gcloud_credentials.to_json())
    old_credentials["token"] = "some-token"
    app_cache["youtube-api-credentials"] = json.dumps(old_credentials)
    mocker.patch.object(
        Credentials,
        "valid",
        new_callable=mocker.PropertyMock,
        return_value=False,
    )

    authenticator()

    assert json.loads(app_cache["youtube-api-credentials"]) == json.loads(
        gcloud_credentials.to_json()
    )


@pytest.mark.usefixtures("credentials_cache")
def test_skip_fetch_if_valid_credentials_cache_exist(
    mocker,
    authenticator,
    run_local_server_mock,
):
    mocker.patch.object(
        Credentials,
        "valid",
        new_callable=mocker.PropertyMock,
        return_value=True,
    )

    authenticator()

    run_local_server_mock.assert_not_called()


@pytest.mark.usefixtures("credentials_cache")
def test_authenticate_from_cache(authenticator, gcloud_credentials):
    result = authenticator()

    assert result.to_json() == gcloud_credentials.to_json()


@pytest.mark.usefixtures("refresh_credentials_mock", "credentials_cache")
def test_refresh_expired_token(mocker, authenticator):
    mocker.patch.object(
        Credentials,
        "expired",
        new_callable=mocker.PropertyMock,
        return_value=True,
    )

    result = authenticator()

    assert result.token == "updated-access-token"
    assert result.refresh_token == "updated-refresh-token"


@pytest.mark.usefixtures("credentials_cache")
def test_get_new_credentials_if_no_refresh_token(
    mocker,
    authenticator,
    run_local_server_mock,
):
    mocker.patch.object(
        Credentials,
        "expired",
        new_callable=mocker.PropertyMock,
        return_value=True,
    )
    mocker.patch.object(
        Credentials,
        "refresh_token",
        new_callable=mocker.PropertyMock,
        return_value=None,
    )

    authenticator()

    run_local_server_mock.assert_called_once()


@pytest.mark.usefixtures("credentials_cache")
def test_valid_credentials_are_returned_from_cache(
    mocker, authenticator, gcloud_credentials
):
    mocker.patch.object(
        Credentials,
        "valid",
        new_callable=mocker.PropertyMock,
        return_value=True,
    )

    result = authenticator()

    assert result.to_json() == gcloud_credentials.to_json()


@pytest.mark.usefixtures("credentials_cache")
def test_get_new_credentials_if_current_are_invalid(
    mocker,
    authenticator,
    run_local_server_mock,
):
    mocker.patch.object(
        Credentials,
        "valid",
        new_callable=mocker.PropertyMock,
        return_value=False,
    )

    authenticator()

    run_local_server_mock.assert_called_once()
