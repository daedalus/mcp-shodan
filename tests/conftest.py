from unittest.mock import MagicMock, patch

import pytest


@pytest.fixture
def mock_shodan_client() -> MagicMock:
    with patch("mcp_shodan.client.shodan.Shodan") as mock:
        client = MagicMock()
        mock.return_value = client
        yield client


@pytest.fixture(autouse=True)
def setup_env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("SHODAN_API_KEY", "test_api_key")
