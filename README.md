# honest-irc-mcp

**MCP server for [quantum-proof messaging + honesty-auth](https://github.com/8b-is/honest-irc)**
over [Model Context Protocol](https://modelcontextprotocol.io) using the protocol version negotiated by the installed SDK.

## Tools

- `msg`
- ` search`
- ` honesty`
- ` verify`
- ` rooms`
- ` peers`
- ` music`
- ` quant`

## Usage

```bash
python -m pip install .
honest-irc-mcp
```

Requires: honest-ircd running on localhost:9667 for tool calls.
Startup and discovery tests run without the daemon: `python -m unittest discover -s tests -v`.
Protocol discovery tests do not verify the daemon's encryption or identity guarantees.

## The 8b-is MCP Ecosystem

| MCP Server | Purpose |
|------------|---------|
| **honest-irc-mcp** | Quantum-proof messaging + honesty-auth |
| **ayeos-mcp** | Ternary matrix inference (LINOSV seed) |
| **mlx-quant-mcp** | Ternary quantization (BitNet b1.58) |
| **bluesky-mcp** | AT Protocol (24 tools) |

**[axiomquant.org](https://axiomquant.org)** · **[pocoo.vaked.dev](https://pocoo.vaked.dev)**
