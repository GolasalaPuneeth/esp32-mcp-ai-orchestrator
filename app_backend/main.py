from fastmcp import FastMCP
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from tools import light,LightDoc,Light
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

light: LightDoc = Light()

mcp.add_tool(light.turn_on_light)
mcp.add_tool(light.get_status)

if __name__ == "__main__":
    mcp.run(transport="http", host="0.0.0.0", port=8003)