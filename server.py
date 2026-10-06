"""honest-irc-mcp — quantum-proof messaging over Model Context Protocol.

Exposes honest-ircd tools as MCP tools:
  - msg: send a DM (private, encrypted, 1:1)
  - search: search public group history
  - honesty: share your honesty vector
  - verify: challenge-verify a peer
  - rooms: list public rooms
  - peers: list connected peers
  - music: share current music.vaked.dev choreography
  - quant: generate shared ternary matrix with a peer

Requires honest-ircd running on localhost:9667.
"""
import asyncio
import json
import socket
from mcp.server.mcpserver import MCPServer

server = MCPServer("honest-irc-mcp")

def _irc_cmd(cmd: str) -> str:
    """Send a command to honest-ircd and return the response."""
    if "\r" in cmd or "\n" in cmd:
        raise ValueError("Command arguments must not contain CR or LF")
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(5)
            sock.connect(("127.0.0.1", 9667))
            sock.recv(1024)  # discard banner
            sock.sendall((cmd + "\n").encode())
            response = b""
            while True:
                try:
                    chunk = sock.recv(4096)
                    if not chunk:
                        break
                    response += chunk
                except socket.timeout:
                    break
            return response.decode().strip()
    except Exception as e:
        return json.dumps({"error": str(e)})

@server.tool()
async def msg(peer: str, text: str) -> str:
    """Send a private DM to a peer."""
    return await asyncio.to_thread(_irc_cmd, f"/msg {peer} {text}")

@server.tool()
async def search(term: str) -> str:
    """Search public group history."""
    return await asyncio.to_thread(_irc_cmd, f"/search {term}")

@server.tool()
async def honesty() -> str:
    """Share your signed honesty vector."""
    return await asyncio.to_thread(_irc_cmd, "/honesty")

@server.tool()
async def verify(peer: str) -> str:
    """Challenge-verify a peer's identity."""
    return await asyncio.to_thread(_irc_cmd, f"/verify {peer}")

@server.tool()
async def rooms() -> str:
    """List all public rooms."""
    return await asyncio.to_thread(_irc_cmd, "/rooms")

@server.tool()
async def peers() -> str:
    """List all connected peers."""
    return await asyncio.to_thread(_irc_cmd, "/peers")

@server.tool()
async def music() -> str:
    """Share current music.vaked.dev choreography."""
    return await asyncio.to_thread(_irc_cmd, "/music")

@server.tool()
async def quant(seed: str = "LINOSV") -> str:
    """Generate a shared ternary matrix with a peer."""
    return await asyncio.to_thread(_irc_cmd, f"/quant {seed}")

def main():
    server.run(transport="stdio")

if __name__ == "__main__":
    main()
