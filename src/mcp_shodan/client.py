import os
from typing import Any

import fastmcp
import shodan

mcp = fastmcp.FastMCP("mcp-shodan")

_client: shodan.Shodan | None = None


def get_client() -> shodan.Shodan:
    global _client
    api_key = os.environ.get("SHODAN_API_KEY", "")
    if not api_key:
        raise ValueError("SHODAN_API_KEY environment variable is not set")
    if _client is None:
        _client = shodan.Shodan(api_key)
    return _client


def set_client(client: shodan.Shodan | None) -> None:
    global _client
    _client = client


@mcp.tool()
def shodan_host(ip: str, history: bool = False, minify: bool = False) -> dict[str, Any]:
    """Get all available information on an IP.

    Args:
        ip: IP address of the computer.
        history: True if you want to grab the historical banners for the host.
        minify: True to only return the list of ports and general host information.

    Returns:
        A dictionary containing all available information on the IP.

    Example:
        >>> shodan_host("1.1.1.1")
        {"ip": "1.1.1.1", "ports": [443, 80], ...}
    """
    client = get_client()
    return client.host(ip, history=history, minify=minify)


@mcp.tool()
def shodan_count(query: str, facets: str | None = None) -> dict[str, Any]:
    """Returns the total number of search results for the query.

    Args:
        query: Search query; identical syntax to the website.
        facets: A list of properties to get summary information on.

    Returns:
        A dictionary with 'total' property and optionally 'facets'.

    Example:
        >>> shodan_count("apache")
        {"total": 1000000, "facets": {...}}
    """
    client = get_client()
    return client.count(query, facets=facets)


@mcp.tool()
def shodan_search(
    query: str,
    page: int = 1,
    limit: int | None = None,
    offset: int | None = None,
    facets: str | None = None,
    minify: bool = True,
) -> dict[str, Any]:
    """Search the SHODAN database.

    Args:
        query: Search query; identical syntax to the website.
        page: Page number of the search results.
        limit: Number of results to return.
        offset: Search offset to begin getting results from.
        facets: A list of properties to get summary information on.
        minify: Whether to minify the banner.

    Returns:
        A dictionary with 'matches' and 'total' properties.

    Example:
        >>> shodan_search("apache", limit=10)
        {"matches": [...], "total": 1000000}
    """
    client = get_client()
    return client.search(
        query,
        page=page,
        limit=limit,
        offset=offset,
        facets=facets,
        minify=minify,
    )


@mcp.tool()
def shodan_search_cursor(
    query: str, minify: bool = True, retries: int = 5
) -> list[dict[str, Any]]:
    """Search the SHODAN database and return an iterator.

    Args:
        query: Search query; identical syntax to the website.
        minify: Whether to minify the banner.
        retries: How often to retry the search in case it times out.

    Returns:
        A list of search results.

    Example:
        >>> list(shodan_search_cursor("nginx"))
        [{...}, {...}]
    """
    client = get_client()
    return list(client.search_cursor(query, minify=minify, retries=retries))


@mcp.tool()
def shodan_alerts(
    aid: str | None = None, include_expired: bool = True
) -> dict[str, Any]:
    """List all of the active alerts that the user created.

    Args:
        aid: Filter by alert ID.
        include_expired: Whether to include expired alerts.

    Returns:
        A dictionary containing the alerts.

    Example:
        >>> shodan_alerts()
        {"alerts": [...]}
    """
    client = get_client()
    return client.alerts(aid=aid, include_expired=include_expired)


@mcp.tool()
def shodan_create_alert(name: str, ip: str, expires: int = 0) -> dict[str, Any]:
    """Create a new alert.

    Args:
        name: Name of the alert.
        ip: IP address or netblock to monitor.
        expires: Number of seconds until the alert expires.

    Returns:
        A dictionary containing the created alert.

    Example:
        >>> shodan_create_alert("My Server", "1.2.3.4")
        {"id": "alert_123", "name": "My Server", ...}
    """
    client = get_client()
    return client.create_alert(name, ip, expires=expires)


@mcp.tool()
def shodan_delete_alert(aid: str) -> dict[str, Any]:
    """Delete the alert with the given ID.

    Args:
        aid: The ID of the alert to delete.

    Returns:
        A dictionary confirming deletion.

    Example:
        >>> shodan_delete_alert("alert_123")
        {"deleted": true}
    """
    client = get_client()
    return client.delete_alert(aid)


@mcp.tool()
def shodan_scan(ips: str, force: bool = False) -> dict[str, Any]:
    """Scan a network using Shodan.

    Args:
        ips: A list of IPs or netblocks in CIDR notation.
        force: Whether to force re-scan (enterprise only).

    Returns:
        A dictionary with scan ID and information.

    Example:
        >>> shodan_scan("1.2.3.4/24")
        {"id": "scan_123", "count": 256, "credits_left": 100}
    """
    client = get_client()
    return client.scan(ips, force=force)


@mcp.tool()
def shodan_scan_internet(port: str, protocol: str) -> dict[str, Any]:
    """Scan the internet using Shodan.

    Args:
        port: The port that should get scanned.
        protocol: The name of the protocol.

    Returns:
        A dictionary with scan ID and information.

    Example:
        >>> shodan_scan_internet("443", "https")
        {"id": "scan_123"}
    """
    client = get_client()
    return client.scan_internet(port, protocol)


@mcp.tool()
def shodan_scan_status(scan_id: str) -> dict[str, Any]:
    """Get the status information about a previously submitted scan.

    Args:
        scan_id: The unique ID for the scan.

    Returns:
        A dictionary with status information.

    Example:
        >>> shodan_scan_status("scan_123")
        {"status": "complete", "progress": 100}
    """
    client = get_client()
    return client.scan_status(scan_id)


@mcp.tool()
def shodan_queries(
    page: int = 1, sort: str = "timestamp", order: str = "desc"
) -> dict[str, Any]:
    """List the search queries that have been shared by other users.

    Args:
        sort: Sort by 'votes' or 'timestamp'.
        order: Order 'asc' or 'desc'.

    Returns:
        A list of saved search queries.

    Example:
        >>> shodan_queries()
        {"matches": [...]}
    """
    client = get_client()
    return client.queries(page=page, sort=sort, order=order)


@mcp.tool()
def shodan_queries_search(query: str, page: int = 1) -> dict[str, Any]:
    """Search the directory of saved search queries in Shodan.

    Args:
        query: The search string to look for.
        page: Page number to iterate over results.

    Returns:
        A list of matching saved search queries.

    Example:
        >>> shodan_queries_search("nginx")
        {"matches": [...]}
    """
    client = get_client()
    return client.queries_search(query, page=page)


@mcp.tool()
def shodan_queries_tags(size: int = 10) -> dict[str, Any]:
    """Get popular query tags.

    Args:
        size: The number of tags to return.

    Returns:
        A list of tags.

    Example:
        >>> shodan_queries_tags()
        {"matches": [...]}
    """
    client = get_client()
    return client.queries_tags(size=size)


@mcp.tool()
def shodan_info() -> dict[str, Any]:
    """Returns information about the current API key.

    Returns:
        A dictionary with API key information.

    Example:
        >>> shodan_info()
        {"plan": "developer", "credits": 100}
    """
    client = get_client()
    return client.info()


@mcp.tool()
def shodan_ports() -> list[int]:
    """Get a list of ports that Shodan crawls.

    Returns:
        An array containing the ports that Shodan crawls for.

    Example:
        >>> shodan_ports()
        [22, 80, 443, ...]
    """
    client = get_client()
    return client.ports()


@mcp.tool()
def shodan_protocols() -> dict[str, str]:
    """Get a list of protocols that the Shodan on-demand scanning API supports.

    Returns:
        A dictionary containing protocol name and description.

    Example:
        >>> shodan_protocols()
        {"http": "HTTP", "ssh": "SSH"}
    """
    client = get_client()
    return client.protocols()


@mcp.tool()
def shodan_services() -> dict[str, str]:
    """Get a list of services that Shodan crawls.

    Returns:
        A dictionary containing ports and service names.

    Example:
        >>> shodan_services()
        {"80": "http", "443": "https"}
    """
    client = get_client()
    return client.services()


@mcp.tool()
def shodan_exploits_count(query: str, facets: str | None = None) -> dict[str, Any]:
    """Search the Shodan Exploits archive and return total count.

    Args:
        query: The exploit search query.
        facets: A list of properties to get summary information on.

    Returns:
        A dictionary with total count and facets.

    Example:
        >>> shodan_exploits_count("cve:2024")
        {"total": 1000, "facets": {...}}
    """
    client = get_client()
    return client.exploits.count(query, facets=facets)


@mcp.tool()
def shodan_exploits_search(
    query: str,
    page: int = 1,
    facets: str | None = None,
) -> dict[str, Any]:
    """Search the Shodan Exploits archive.

    Args:
        query: The exploit search query.
        page: The page number to access.
        facets: A list of properties to get summary information on.

    Returns:
        A dictionary containing the results.

    Example:
        >>> shodan_exploits_search("cve:2024")
        {"matches": [...], "total": 1000}
    """
    client = get_client()
    return client.exploits.search(query, page=page, facets=facets)


@mcp.tool()
def shodan_search_tokens(query: str) -> dict[str, Any]:
    """Returns information about the search query itself.

    Args:
        query: Search query; identical syntax to the website.

    Returns:
        A dictionary with filters, errors, attributes and string.

    Example:
        >>> shodan_search_tokens("apache port:80")
        {"filters": ["port:80"], "errors": [], ...}
    """
    client = get_client()
    return client.search_tokens(query)
