from fastmcp import FastMCP
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from tools import LightDoc,Light,MailServiceDoc,MailService
from contextlib import asynccontextmanager

light_obj: LightDoc = Light()

@asynccontextmanager
async def lifespan(server):
    async with light_obj:
        yield

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

# light_obj: LightDoc = Light()
mail_obj: MailServiceDoc = MailService()

mcp.add_tool(light_obj.turn_on_light)
mcp.add_tool(light_obj.get_status)
mcp.add_tool(light_obj.blink_light)
mcp.add_tool(mail_obj.send_html_email)


if __name__ == "__main__":
    mcp.run(transport="http", host="0.0.0.0", port=8003)