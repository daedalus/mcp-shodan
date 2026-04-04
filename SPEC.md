# SPEC.md — mcp-shodan

## Purpose

An MCP (Model Context Protocol) server that exposes all the functionality of the Shodan 1.31.0 API. This server provides tools for searching the Shodan database, managing alerts, accessing exploit information, and more.

## Scope

- All REST API endpoints from shodan-python 1.31.0
- All Exploits API endpoints
- Streaming API access
- MCP protocol implementation using fastmcp

## Public API / Interface

### MCP Tools

All tools are exposed via fastmcp and follow the naming convention `shodan_<method_name>`.

#### Host Information
- `shodan_host(ip, history, minify)` - Get all available information on an IP
- `shodan_count(query, facets)` - Returns total number of search results
- `shodan_search(query, page, limit, offset, facets, minify)` - Search the SHODAN database
- `shodan_search_cursor(query, minify, retries)` - Iterator for search results

#### Alert Management
- `shodan_alerts(aid, include_expired)` - List all active alerts
- `shodan_create_alert(name, ip, expires)` - Create a new alert
- `shodan_delete_alert(aid)` - Delete an alert

#### Scanning
- `shodan_scan(ips, force)` - Scan a network using Shodan
- `shodan_scan_internet(port, protocol)` - Scan the internet
- `shodan_scan_status(scan_id)` - Get status of a scan

#### Directory/Queries
- `shodan_queries(page, sort, order)` - List shared search queries
- `shodan_queries_search(query, page)` - Search saved queries
- `shodan_queries_tags(size)` - Get popular query tags

#### API Information
- `shodan_info()` - Returns API key information
- `shodan_ports()` - Get list of ports that Shodan crawls
- `shodan_protocols()` - Get list of protocols for on-demand scanning
- `shodan_services()` - Get list of services that Shodan crawls

#### Exploits
- `shodan_exploits_count(query, facets)` - Count exploits
- `shodan_exploits_search(query, page, facets)` - Search exploits

#### Query Analysis
- `shodan_search_tokens(query)` - Returns information about search query

## Data Formats

All methods return JSON-serializable dictionaries matching the Shodan API response format.

## Edge Cases

1. Invalid API key raises APIError
2. Network timeout should be handled gracefully
3. Empty search results return empty matches array
4. Rate limiting should be respected
5. Invalid IP format should raise ValueError

## Performance & Constraints

- API key required for all operations
- Rate limits apply based on API plan
- Streaming connections need proper cleanup
