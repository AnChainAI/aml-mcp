# MCP Server For Anti Money Laundering - AnChain.AI

A Model Context Protocol (MCP) server that provides access to global sanctions, IP addresses and blockchain risk data through the [Anchain.ai AML API](https://aml.anchainai.com/). This server enables LLM / AI agents to screen cryptocurrency addresses, check sanctions lists, and assess IP address risks for compliance and security purposes. We welcome questions, comments, and partnership: info AT Anchain.ai 🚀

## Features

- **Cryptocurrency Address Screening**: Screen crypto addresses for risk factors and sanctions compliance across multiple blockchains
- **Sanctions List Screening**: Check individuals, companies, vessels, aircraft, and crypto entities against global sanctions lists
- **IP Address Risk Assessment**: Determine if IP addresses originate from sanctioned countries
- **Multi-Protocol Support**: Supports Bitcoin, Ethereum, Solana, and 10+ other major blockchains

## Supported Blockchains

| Protocol | Name | Code |
|----------|------|------|
| Bitcoin | Bitcoin | `btc` |
| Ethereum | Ethereum | `eth` |
| Solana | Solana | `sol` |
| Stellar | Stellar | `xlm` |
| Tron | Tron | `trx` |
| Elrond | Elrond | `egld` |
| Ripple | Ripple | `xrp` |
| Bitcoin Cash | Bitcoin Cash | `bch` |
| Litecoin | Litecoin | `ltc` |
| Algorand | Algorand | `algo` |
| Bitcoin SV | Bitcoin SV | `bsv` |
| Dash | Dash | `dash` |
| Verge Currency | Verge Currency | `xvg` |
| Zcash | Zcash | `zec` |

## Installation

### Prerequisites

- Python 3.12+
- [uv](https://docs.astral.sh/uv/) package manager
- API key from [Anchain.ai](https://aml.anchainai.com)

#### Installing Python 3.12+

**macOS:**
```bash
# Using Homebrew
brew install python@3.12

# Or download from python.org
# Visit https://www.python.org/downloads/
```

**Linux (Ubuntu/Debian):**
```bash
# Using apt
sudo apt update
sudo apt install python3.12 python3.12-venv python3.12-dev

# Or using pyenv
curl https://pyenv.run | bash
pyenv install 3.12.0
pyenv global 3.12.0
```

**Windows:**
```bash
# Download from python.org
# Visit https://www.python.org/downloads/

# Or using winget
winget install Python.Python.3.12
```

#### Installing uv

**All platforms:**
```bash
# Using pip
pip install uv

# Or using the official installer
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Windows (PowerShell):**
```powershell
# Using the official installer
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### Install from source

```bash
git clone https://github.com/AnChainAI/aml-mcp.git
cd aml-mcp
uv sync
```

The project should now be ready to run.

## Configuration

### MCP Client Configuration

Add the server to your MCP client configuration:

#### Claude Desktop

Add the following to your `claude_desktop_config.json`. Two values are required:

- Replace `/path/to/your/aml-mcp` with the absolute path to your local clone of this repository.
- Replace `your_api_key_here` with your API key from [aml.anchainai.com](https://aml.anchainai.com).

JSON does not allow comments, so keep the file free of `//` or `#` notes.

```json
{
  "mcpServers": {
    "anchain_aml_mcp": {
      "command": "uv",
      "args": [
        "run",
        "--directory",
        "/path/to/your/aml-mcp",
        "--",
        "mcp_server.py",
        "--ANCHAIN_APIKEY",
        "your_api_key_here"
      ]
    }
  }
}
```

##### Alternative: API key from an environment variable

If the `--ANCHAIN_APIKEY` argument is not passed, `mcp_server.py` reads the key from the `ANCHAIN_APIKEY` environment variable. This keeps the key out of the `args` list:

```json
{
  "mcpServers": {
    "anchain_aml_mcp": {
      "command": "uv",
      "args": [
        "run",
        "--directory",
        "/path/to/your/aml-mcp",
        "--",
        "mcp_server.py"
      ],
      "env": {
        "ANCHAIN_APIKEY": "your_api_key_here"
      }
    }
  }
}
```

#### Other MCP Clients

For other MCP clients, use the stdio transport and start the server with `uv run`:

```bash
uv run --directory /path/to/your/aml-mcp -- mcp_server.py --ANCHAIN_APIKEY your_api_key_here
```

Or, with the key in the `ANCHAIN_APIKEY` environment variable:

```bash
uv run --directory /path/to/your/aml-mcp -- mcp_server.py
```

A typical stdio client configuration looks like this (the exact format depends on your client):

```json
{
  "name": "aml",
  "transport": {
    "type": "stdio",
    "command": "uv",
    "args": ["run", "--directory", "/path/to/your/aml-mcp", "--", "mcp_server.py"],
    "env": {
      "ANCHAIN_APIKEY": "your_api_key_here"
    }
  }
}
```

## Usage

Once configured, the server provides eight tools (see the [API Reference](#api-reference)). The three main ones are:

### 1. Cryptocurrency Address Screening

Screen crypto addresses for risk factors and sanctions compliance:

```
Screen address: 0xf4548503dd51de15e8d0e6fb559f6062d38667e7 (eth)
```

### 2. Sanctions List Screening

Check entities against global sanctions lists:

```
Check sanctions for: John Doe, nationality US, born 1980
```

Parameters:
- `schema`: Entity type (person, company, vessel, aircraft, crypto)
- `name`: Full name(s) to search
- `idNumber`: Government ID or passport number(s)
- `nationality`: 2-letter country codes (ISO 3166-1)
- `birthYear`: Birth year(s)
- `scope`: Search scope (basic/full - full requires enterprise plan)

### 3. IP Address Screening

Check if IP addresses originate from sanctioned countries:

```
Check IP: 37.19.90.65
```

## API Reference

### Functions

#### `crypto_screening(address, protocol)`
Screen cryptocurrency addresses for risk factors.

**Parameters:**
- `address` (string): Crypto address to screen
- `protocol` (string): 3-letter blockchain protocol code

**Returns:** Risk assessment including sanctions matches, risk scores, and compliance flags.

#### `sanctions_screening(schema?, name?, idNumber?, nationality?, birthYear?, scope?)`
Screen entities against global sanctions lists.

**Parameters:**
- `schema` (string): Entity type (default: "person")
- `name` (array): Names to search
- `idNumber` (array): ID numbers to search
- `nationality` (array): Country codes to search
- `birthYear` (array): Birth years to search
- `scope` (string): Search scope - "basic" or "full" (default: "basic")

**Returns:** Sanctions matches with entity details and list sources.

#### `ip_screening(ip_address)`
Check IP address country origin against sanctions lists.

**Parameters:**
- `ip_address` (string): IPv4 or IPv6 address to check

**Returns:** Country information and sanctions status.

#### `crypto_activity_screening(address, protocol)`
Analyze a cryptocurrency address for suspicious activity.

**Parameters:**
- `address` (string): Crypto address to analyze
- `protocol` (string): 3-letter blockchain protocol code

#### `crypto_attribution_screening(address, protocol)`
Attribute the transaction flows of a cryptocurrency address. Requires a pro plan API key.

**Parameters:**
- `address` (string): Crypto address to analyze
- `protocol` (string): 3-letter blockchain protocol code

#### `auto_trace(protocol, time_from, time_to, address?, txn_hash?, direction?, time_window?, min_amount?, max_amount?, token?)`
Trace the flow of assets into or out of an address or transaction.

**Parameters:**
- `protocol` (string): One of `btc`, `eth`, `xrp`, `egld`, `trx`
- `time_from` (integer): Start of the trace, as a Unix timestamp
- `time_to` (integer): End of the trace, as a Unix timestamp
- `address` (string): Address to trace (required if `txn_hash` is not given)
- `txn_hash` (string): Transaction hash to trace (required if `address` is not given)
- `direction` (string): `"in"` for incoming or `"out"` for outgoing (default: `"in"`)
- `time_window` (integer): Days to include around the transaction time (default: 365)
- `min_amount` (integer): Minimum transaction amount to include (default: 0)
- `max_amount` (integer): Maximum transaction amount to include
- `token` (string): Token contract address to trace, on EVM chains

**Returns:** `path_info` (the traced transactions, each with depth, hash, sender, receiver, timestamp and amount), plus `token_mapping` and `labels_mapping` for resolving token and known-entity addresses.

#### `get_source_code(address, protocol)`
Get a smart contract's source code, if available.

**Parameters:**
- `address` (string): Smart contract address
- `protocol` (string): `eth` or `bnb`

#### `get_transaction(transaction_hash, protocol, scope?)`
Get the data for a transaction.

**Parameters:**
- `transaction_hash` (string): Transaction hash
- `protocol` (string): `eth` or `bnb`
- `scope` (string): `"summary"` for a summarized analysis, or `"full"` for the full execution flow (default: `"summary"`). Full scope can return a very large response.

**Returns:** With `summary`: overview, token and address mappings, balance changes, the transaction graph and a summary of key events. With `full`: the call-by-call execution flow.

## Examples

In an MCP client such as Claude Desktop, you call these tools by asking in plain language. The assistant picks the right tool and parameters.

### Address Risk Assessment

> Screen the Bitcoin address bc1qxy2kgdygjrsqtzq2n0yrf2493p83kkfjhx0wlh and summarize its risk.

### Sanctions Screening

> Check John Doe and Jane Smith against sanctions lists. They are persons with US or Canadian nationality. Use the basic scope.

### IP Geolocation Check

> Does the IP address 8.8.8.8 come from a sanctioned country?

### Python Example

You can also call the tools from Python with the [FastMCP](https://gofastmcp.com) client, which is already a dependency of this project. Set `ANCHAIN_APIKEY` in your environment first.

```python
import asyncio
import os

from fastmcp import Client

config = {
    "mcpServers": {
        "anchain_aml": {
            "command": "uv",
            "args": ["run", "--directory", "/path/to/your/aml-mcp", "--", "mcp_server.py"],
            "env": {"ANCHAIN_APIKEY": os.environ["ANCHAIN_APIKEY"]},
        }
    }
}


async def main():
    async with Client(config) as client:
        # Screen a Bitcoin address
        address = await client.call_tool(
            "crypto_screening",
            {"address": "bc1qxy2kgdygjrsqtzq2n0yrf2493p83kkfjhx0wlh", "protocol": "btc"},
        )
        print(address.data)

        # Check multiple individuals against sanctions lists
        sanctions = await client.call_tool(
            "sanctions_screening",
            {
                "schema": "person",
                "name": ["John Doe", "Jane Smith"],
                "nationality": ["us", "ca"],
                "scope": "basic",
            },
        )
        print(sanctions.data)

        # Check where an IP address comes from
        ip = await client.call_tool("ip_screening", {"ip_address": "8.8.8.8"})
        print(ip.data)


asyncio.run(main())
```

## Error Handling

The server handles various error conditions:
- Invalid API keys
- Unsupported blockchain protocols
- Malformed addresses or parameters
- Rate limiting
- Network connectivity issues

For common problems and fixes, see [TROUBLESHOOTING.md](TROUBLESHOOTING.md).

## Rate Limits

Please refer to the [Anchain.ai API documentation](https://aml.anchainai.com/pricing) for current rate limits and pricing information.

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

- **Documentation**: [Anchain.ai API Docs](https://aml.anchainai.com/docs)
- **Issues**: [GitHub Issues](https://github.com/yourusername/mcp-aml-server/issues)
- **API Support**: Contact Info AT Anchain.ai 

## Disclaimer

This tool is provided for compliance and security research purposes. Users are responsible for ensuring compliance with all applicable laws and regulations. The accuracy of risk assessments and sanctions data depends on the underlying Anchain.ai API service.
