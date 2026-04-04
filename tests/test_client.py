from unittest.mock import MagicMock

import pytest

import mcp_shodan.client as client_module


@pytest.fixture(autouse=True)
def reset_client() -> None:
    yield
    client_module.set_client(None)


def test_get_client_success(mock_shodan_client: MagicMock) -> None:
    result = client_module.get_client()
    assert result == mock_shodan_client


def test_get_client_no_api_key(monkeypatch: pytest.MonkeyPatch) -> None:
    client_module.set_client(None)
    monkeypatch.delenv("SHODAN_API_KEY", raising=False)
    with pytest.raises(ValueError, match="SHODAN_API_KEY"):
        client_module.get_client()


def test_shodan_host(mock_shodan_client: MagicMock) -> None:
    mock_shodan_client.host.return_value = {"ip": "1.1.1.1", "ports": [443]}
    result = client_module.shodan_host("1.1.1.1")
    assert result == {"ip": "1.1.1.1", "ports": [443]}
    mock_shodan_client.host.assert_called_once_with(
        "1.1.1.1", history=False, minify=False
    )


def test_shodan_host_with_options(mock_shodan_client: MagicMock) -> None:
    mock_shodan_client.host.return_value = {"ip": "1.1.1.1"}
    client_module.shodan_host("1.1.1.1", history=True, minify=True)
    mock_shodan_client.host.assert_called_once_with(
        "1.1.1.1", history=True, minify=True
    )


def test_shodan_count(mock_shodan_client: MagicMock) -> None:
    mock_shodan_client.count.return_value = {"total": 1000}
    result = client_module.shodan_count("apache")
    assert result == {"total": 1000}
    mock_shodan_client.count.assert_called_once_with("apache", facets=None)


def test_shodan_count_with_facets(mock_shodan_client: MagicMock) -> None:
    mock_shodan_client.count.return_value = {"total": 1000, "facets": {}}
    client_module.shodan_count("apache", facets="country")
    mock_shodan_client.count.assert_called_once_with("apache", facets="country")


def test_shodan_search(mock_shodan_client: MagicMock) -> None:
    mock_shodan_client.search.return_value = {"matches": [], "total": 0}
    result = client_module.shodan_search("apache")
    assert result == {"matches": [], "total": 0}


def test_shodan_search_with_params(mock_shodan_client: MagicMock) -> None:
    mock_shodan_client.search.return_value = {"matches": [], "total": 0}
    client_module.shodan_search(
        "apache", page=2, limit=10, offset=5, facets="os", minify=False
    )
    mock_shodan_client.search.assert_called_once_with(
        "apache", page=2, limit=10, offset=5, facets="os", minify=False
    )


def test_shodan_search_cursor(mock_shodan_client: MagicMock) -> None:
    mock_cursor = [{"ip": "1.1.1.1"}, {"ip": "2.2.2.2"}]
    mock_shodan_client.search_cursor.return_value = iter(mock_cursor)
    result = client_module.shodan_search_cursor("nginx")
    assert result == mock_cursor


def test_shodan_alerts(mock_shodan_client: MagicMock) -> None:
    mock_shodan_client.alerts.return_value = {"alerts": []}
    result = client_module.shodan_alerts()
    assert result == {"alerts": []}


def test_shodan_alerts_with_params(mock_shodan_client: MagicMock) -> None:
    mock_shodan_client.alerts.return_value = {"alerts": []}
    client_module.shodan_alerts(aid="alert_123", include_expired=False)
    mock_shodan_client.alerts.assert_called_once_with(
        aid="alert_123", include_expired=False
    )


def test_shodan_create_alert(mock_shodan_client: MagicMock) -> None:
    mock_shodan_client.create_alert.return_value = {"id": "alert_123", "name": "Test"}
    result = client_module.shodan_create_alert("Test", "1.2.3.4")
    assert result == {"id": "alert_123", "name": "Test"}
    mock_shodan_client.create_alert.assert_called_once_with(
        "Test", "1.2.3.4", expires=0
    )


def test_shodan_delete_alert(mock_shodan_client: MagicMock) -> None:
    mock_shodan_client.delete_alert.return_value = {"deleted": True}
    result = client_module.shodan_delete_alert("alert_123")
    assert result == {"deleted": True}
    mock_shodan_client.delete_alert.assert_called_once_with("alert_123")


def test_shodan_scan(mock_shodan_client: MagicMock) -> None:
    mock_shodan_client.scan.return_value = {"id": "scan_123"}
    result = client_module.shodan_scan("1.2.3.4/24")
    assert result == {"id": "scan_123"}
    mock_shodan_client.scan.assert_called_once_with("1.2.3.4/24", force=False)


def test_shodan_scan_internet(mock_shodan_client: MagicMock) -> None:
    mock_shodan_client.scan_internet.return_value = {"id": "scan_123"}
    result = client_module.shodan_scan_internet("443", "https")
    assert result == {"id": "scan_123"}
    mock_shodan_client.scan_internet.assert_called_once_with("443", "https")


def test_shodan_scan_status(mock_shodan_client: MagicMock) -> None:
    mock_shodan_client.scan_status.return_value = {"status": "complete"}
    result = client_module.shodan_scan_status("scan_123")
    assert result == {"status": "complete"}
    mock_shodan_client.scan_status.assert_called_once_with("scan_123")


def test_shodan_queries(mock_shodan_client: MagicMock) -> None:
    mock_shodan_client.queries.return_value = {"matches": []}
    result = client_module.shodan_queries()
    assert result == {"matches": []}


def test_shodan_queries_with_params(mock_shodan_client: MagicMock) -> None:
    mock_shodan_client.queries.return_value = {"matches": []}
    client_module.shodan_queries(page=2, sort="votes", order="asc")
    mock_shodan_client.queries.assert_called_once_with(
        page=2, sort="votes", order="asc"
    )


def test_shodan_queries_search(mock_shodan_client: MagicMock) -> None:
    mock_shodan_client.queries_search.return_value = {"matches": []}
    result = client_module.shodan_queries_search("nginx")
    assert result == {"matches": []}


def test_shodan_queries_tags(mock_shodan_client: MagicMock) -> None:
    mock_shodan_client.queries_tags.return_value = {"matches": []}
    result = client_module.shodan_queries_tags()
    assert result == {"matches": []}


def test_shodan_info(mock_shodan_client: MagicMock) -> None:
    mock_shodan_client.info.return_value = {"plan": "developer"}
    result = client_module.shodan_info()
    assert result == {"plan": "developer"}


def test_shodan_ports(mock_shodan_client: MagicMock) -> None:
    mock_shodan_client.ports.return_value = [80, 443]
    result = client_module.shodan_ports()
    assert result == [80, 443]


def test_shodan_protocols(mock_shodan_client: MagicMock) -> None:
    mock_shodan_client.protocols.return_value = {"http": "HTTP"}
    result = client_module.shodan_protocols()
    assert result == {"http": "HTTP"}


def test_shodan_services(mock_shodan_client: MagicMock) -> None:
    mock_shodan_client.services.return_value = {"80": "http"}
    result = client_module.shodan_services()
    assert result == {"80": "http"}


def test_shodan_exploits_count(mock_shodan_client: MagicMock) -> None:
    mock_shodan_client.exploits.count.return_value = {"total": 100}
    result = client_module.shodan_exploits_count("cve:2024")
    assert result == {"total": 100}


def test_shodan_exploits_search(mock_shodan_client: MagicMock) -> None:
    mock_shodan_client.exploits.search.return_value = {"matches": [], "total": 0}
    result = client_module.shodan_exploits_search("cve:2024")
    assert result == {"matches": [], "total": 0}


def test_shodan_search_tokens(mock_shodan_client: MagicMock) -> None:
    mock_shodan_client.search_tokens.return_value = {"filters": []}
    result = client_module.shodan_search_tokens("apache")
    assert result == {"filters": []}
