from mock import mock

from app.common.local import check_if_local


@mock.patch("os.environ.get", return_value=False)
def test_check_if_local_on_prod(mocked_env_get):
    assert not check_if_local(), "Prod isn't local at all"
    mocked_env_get.assert_called_once_with("IS_LOCAL")


@mock.patch("os.environ.get", side_effect=lambda key: key == "IS_LOCAL")
def test_check_if_local_on_local(mocked_env_get):
    assert check_if_local(), "Pytest request.host is localhost by default"

    with mock.patch("app.common.local.request") as m_request:
        m_request.remote_addr = "127.0.0.1"
        assert check_if_local(), "Remote address is local"

    with mock.patch("app.common.local.request") as m_request:
        m_request.host = "localhost:5000"
        assert check_if_local(), "Hostname is localhost"

        m_request.host = "127.0.0.1:5000"
        assert check_if_local(), "Hostname is loopback ip"

        m_request.host = "not localhost"
        assert not check_if_local(), "Host is not localhost"

        mocked_env_get.side_effect = lambda key: key in ("IS_LOCAL", "VPN")
        assert check_if_local(), "Treat VPN as local"
