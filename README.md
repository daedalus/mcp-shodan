# mcp-shodan

MCP server exposing [Shodan](https://www.shodan.io/) API functionality via the Model Context Protocol.

[![PyPI](https://img.shields.io/pypi/v/mcp-shodan.svg)](https://pypi.org/project/mcp-shodan/)
[![Python](https://img.shields.io/pypi/pyversions/mcp-shodan.svg)](https://pypi.org/project/mcp-shodan/)
[![Coverage](https://codecov.io/gh/daedalus/mcp-shodan/branch/main/graph/badge.svg)](https://codecov.io/gh/daedalus/mcp-shodan)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

## Install

```bash
pip install mcp-shodan
```

## Usage

```bash
export SHODAN_API_KEY=your_api_key
mcp-shodan
```

Or add to your MCP configuration:

```json
{
  "mcpServers": {
    "shodan": {
      "command": "mcp-shodan",
      "env": {
        "SHODAN_API_KEY": "your_api_key"
      }
    }
  }
}
```

## Available Tools

### Host Information
- `shodan_host` - Get all available information on an IP address

### Search
- `shodan_search` - Search the Shodan database
- `shodan_search_cursor` - Search and return an iterator
- `shodan_count` - Get total number of search results
- `shodan_search_tokens` - Get information about a search query

### Alerts
- `shodan_alerts` - List all active alerts
- `shodan_create_alert` - Create a new alert
- `shodan_delete_alert` - Delete an alert

### Scanning
- `shodan_scan` - Scan a network
- `shodan_scan_internet` - Scan the internet on a port
- `shodan_scan_status` - Get scan status

### Saved Queries
- `shodan_queries` - List shared search queries
- `shodan_queries_search` - Search saved queries
- `shodan_queries_tags` - Get popular query tags

### Exploits
- `shodan_exploits_search` - Search the Shodan Exploits archive
- `shodan_exploits_count` - Get total exploit count

### Utilities
- `shodan_info` - Get API key information
- `shodan_ports` - Get list of ports Shodan crawls
- `shodan_protocols` - Get supported protocols
- `shodan_services` - Get list of services

## Example

```python
# Get information about a host
shodan_host("1.1.1.1")

# Search for specific services
shodan_search("apache", limit=10)

# Count results for a query
shodan_count("nginx")

# Check your API plan
shodan_info()
```

mcp-name: io.github.daedalus/mcp-shodan
