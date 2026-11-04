# Troubleshooting

Common problems when setting up and using the AnChain.AI AML MCP server, and how to fix them.

## Missing or invalid API key

**Symptoms**

- The server exits on startup with `ANCHAIN_APIKEY environment variable is required`.
- The server starts, but every tool call returns an authentication error from the API.

**Fixes**

- Make sure a key is provided in one of two ways:
  - the `--ANCHAIN_APIKEY your_api_key_here` argument, or
  - the `ANCHAIN_APIKEY` environment variable (for Claude Desktop, put it in the server's `"env"` block).

  If both are set, the command-line argument wins.
- Check that the placeholder `your_api_key_here` was actually replaced with your key.
- Copy the key again from [aml.anchainai.com](https://aml.anchainai.com) and make sure it has no extra spaces, quotes, or line breaks.
- Confirm that your plan covers the tool you are calling. For example, `crypto_attribution_screening` needs a pro plan key, and the `full` scope of `sanctions_screening` needs an enterprise plan.
- After changing the key, fully restart your MCP client so it relaunches the server.

## Unsupported protocol code

**Symptoms**

- The crypto screening tools return an error about the protocol, or no useful result.

**Fixes**

The `protocol` argument must be one of these 14 lowercase codes:

| Code | Blockchain |
|------|------------|
| `btc` | Bitcoin |
| `eth` | Ethereum |
| `sol` | Solana |
| `xlm` | Stellar |
| `trx` | Tron |
| `egld` | Elrond (MultiversX) |
| `xrp` | Ripple |
| `bch` | Bitcoin Cash |
| `ltc` | Litecoin |
| `algo` | Algorand |
| `bsv` | Bitcoin SV |
| `dash` | Dash |
| `xvg` | Verge Currency |
| `zec` | Zcash |

Things to check:

- Use the code, not the full name or ticker in caps: `btc`, not `Bitcoin` or `BTC`.
- Make sure the address matches the protocol. An Ethereum address (`0x...`) sent with `btc` will not screen correctly.
- Some tools support fewer protocols:
  - `auto_trace`: `btc`, `eth`, `xrp`, `egld`, `trx`
  - `get_source_code` and `get_transaction`: `eth`, `bnb`

## Python 3.12 and uv setup

The project needs Python 3.12 or newer and the [uv](https://docs.astral.sh/uv/) package manager.

**`uv: command not found`**

- Install uv by following the steps in the [README](README.md#installing-uv), then open a new terminal.
- Check with `uv --version`.

**Wrong Python version**

- uv can install a suitable Python for you:

  ```bash
  uv python install 3.12
  ```

- Then, from the repository folder, set up the environment:

  ```bash
  uv sync
  ```

- If `uv sync` reports that the Python version does not satisfy `requires-python = ">=3.12"`, run `uv python list` to see which versions uv can find.

**Claude Desktop cannot find `uv`**

Claude Desktop does not always use the same `PATH` as your terminal, so `"command": "uv"` may fail even though `uv` works in your shell. Use the full path to `uv` instead:

- macOS/Linux: run `which uv` and use the result, for example `/Users/you/.local/bin/uv`.
- Windows: run `where uv` and use the result, with backslashes escaped in JSON, for example `C:\\Users\\you\\.local\\bin\\uv.exe`.

**Test the server outside your MCP client**

Run the server directly to see any startup errors:

```bash
uv run --directory /path/to/your/aml-mcp -- mcp_server.py --ANCHAIN_APIKEY your_api_key_here
```

If it starts and waits for input without errors, the setup is working. Press `Ctrl+C` to stop it.

## Invalid JSON in the Claude Desktop config

**Symptoms**

- Claude Desktop shows a config error on startup, or the AML tools do not appear.

**Fixes**

- **Remove comments.** JSON does not allow `//` or `/* */` comments.
- **Remove trailing commas.** There must be no comma after the last item in a list or object.
- **Use double quotes** for all keys and strings, not single quotes.
- **Escape backslashes in Windows paths**: `"C:\\Users\\you\\aml-mcp"`, or use forward slashes: `"C:/Users/you/aml-mcp"`.
- **Merge, don't duplicate.** If your config already has an `"mcpServers"` object, add `"anchain_aml_mcp"` inside it rather than adding a second `"mcpServers"` key.
- **Validate the file** before restarting Claude Desktop:

  ```bash
  python -m json.tool claude_desktop_config.json
  ```

  This prints the formatted file if it is valid, or the line and column of the first error if it is not.

The config file lives at:

- macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
- Windows: `%APPDATA%\Claude\claude_desktop_config.json`

A known-good example is in [`claude_desktop_config_sample.json`](claude_desktop_config_sample.json).
