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
import json
import socket
from mcp.server import Server
from mcp.server.stdio import stdio_server

server = Server("honest-irc-mcp")

def _irc_cmd(cmd: str) -> str:
    """Send a command to honest-ircd and return the response."""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
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
        sock.close()
        return response.decode().strip()
    except Exception as e:
        return json.dumps({"error": str(e)})

@server.tool()
async def msg(peer: str, text: str) -> str:
    """Send a private DM to a peer."""
    return _irc_cmd(f"/msg {peer} {text}")

@server.tool()
async def search(term: str) -> str:
    """Search public group history."""
    return _irc_cmd(f"/search {term}")

@server.tool()
async def honesty() -> str:
    """Share your signed honesty vector."""
    return _irc_cmd("/honesty")

@server.tool()
async def verify(peer: str) -> str:
    """Challenge-verify a peer's identity."""
    return _irc_cmd(f"/verify {peer}")

@server.tool()
async def rooms() -> str:
    """List all public rooms."""
    return _irc_cmd("/rooms")

@server.tool()
async def peers() -> str:
    """List all connected peers."""
    return _irc_cmd("/peers")

@server.tool()
async def music() -> str:
    """Share current music.vaked.dev choreography."""
    return _irc_cmd("/music")

@server.tool()
async def quant(seed: str = "LINOSV") -> str:
    """Generate a shared ternary matrix with a peer."""
    return _irc_cmd(f"/quant {seed}")

async def main():
    async with stdio_server() as (read, write):
        await server.run(read, write, server.create_initialization_options())

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
