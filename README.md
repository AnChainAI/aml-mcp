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

Add to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "anchain_aml_mcp": {
      "command": "uv",
      "args": [
        "run",
        "--directory",
        "/path/to/your/aml-mcp",  // Required - change to your local path
        "--",
        "mcp_server.py",
        "--ANCHAIN_APIKEY", 
        "your_api_key_here"  // Required - get your API key at https://aml.anchainai.com
      ]
    }
  }
}
```

#### Other MCP Clients

For other MCP clients, use the stdio transport:

```json
{
  "name": "aml",
  "transport": {
    "type": "stdio",
    "command": "mcp-aml-server"
  }
}
```

## Usage

Once configured, the server provides three main functions:

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

#### `crypto_screening(address, proto)`
Screen cryptocurrency addresses for risk factors.

**Parameters:**
- `address` (string): Crypto address to screen
- `proto` (string): 3-letter blockchain protocol code

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

## Examples

### Address Risk Assessment
```javascript
// Screen a Bitcoin address
const result = await crypto_screening(
  "bc1qxy2kgdygjrsqtzq2n0yrf2493p83kkfjhx0wlh", 
  "btc"
);
```

### Sanctions Screening
```javascript
// Check multiple individuals
const result = await sanctions_screening({
  schema: "person",
  name: ["John Doe", "Jane Smith"],
  nationality: ["us", "ca"],
  scope: "basic"
});
```

### IP Geolocation Check
```javascript
// Check IP origin
const result = await ip_screening("8.8.8.8");
```

## Error Handling

The server handles various error conditions:
- Invalid API keys
- Unsupported blockchain protocols
- Malformed addresses or parameters
- Rate limiting
- Network connectivity issues

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
