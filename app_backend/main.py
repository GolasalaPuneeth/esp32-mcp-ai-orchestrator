from fastmcp import FastMCP
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware

mcp = FastMCP("My MCP Server")

middleware = [
    Middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Allow all origins; use specific origins for security
        allow_methods=["GET", "POST", "DELETE", "OPTIONS"],
        allow_headers=[
            "mcp-protocol-version",
            "mcp-session-id",
            "Authorization",
            "Content-Type",
        ],
        expose_headers=["mcp-session-id"],
    )
]

mcp.http_app(middleware=middleware)

@mcp.tool
def greet(name: str) -> str:
    """Greet a person by name."""
    print("Using--------->greet")
    return f"Hello, {name}!"


@mcp.tool
def echo_text(text: str) -> str:
    """Return the supplied text unchanged."""
    print("Using--------->echo")
    return text


@mcp.tool
def add_numbers(a: float, b: float) -> float:
    """Add two numbers and return their sum."""
    print("Using--------->add number")

    return a + b


@mcp.tool
def server_status() -> str:
    """Return a simple status message to confirm the server is responding."""
    print("Using--------->server status")

    return "MCP server is working."


if __name__ == "__main__":
    mcp.run(transport="http", host="0.0.0.0", port=8003)