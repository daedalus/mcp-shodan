# mcp-shodan

MCP server exposing all Shodan API functionality.

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

## API

See the [Shodan API documentation](https://developer.shodan.io/api) for details.

mcp-name: io.github.daedalus/mcp-shodan
