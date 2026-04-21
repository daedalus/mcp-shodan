# MCP Shodan

MCP server exposing Shodan API functionality.

## When to use this skill

Use this skill when you need to:
- Search for internet-connected devices
- Get host information
- Use Shodan alerts
- Search for exploits

## Tools

**Host Information:**
- `shodan_host` - Get info on an IP

**Search:**
- `shodan_search`, `shodan_search_cursor`
- `shodan_count`, `shodan_search_tokens`

**Alerts:**
- `shodan_alerts`, `shodan_create_alert`, `shodan_delete_alert`

**Scanning:**
- `shodan_scan`, `shodan_scan_internet`, `shodan_scan_status`

**Saved Queries:**
- `shodan_queries`, `shodan_queries_search`, `shodan_queries_tags`

**Exploits:**
- `shodan_exploits_search`, `shodan_exploits_count`

**Utilities:**
- `shodan_info`, `shodan_ports`, `shodan_protocols`, `shodan_services`

## Install

```bash
pip install mcp-shodan
```

Requires: `SHODAN_API_KEY` environment variable