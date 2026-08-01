import os
import sys
import asyncio
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_groq import ChatGroq
from dotenv import load_dotenv
load_dotenv()

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
AVIATION_STACK_API_KEY = os.getenv("AVIATIONSTACK_API_KEY")
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")

# This gets the absolute path to your project folder
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
WEATHER_SERVER_PATH = os.path.join(BASE_DIR, "weather_mcp_server.py")

# Direct path to the aviationstack_mcp package directory
AVIATION_SRC_DIR = os.path.join(BASE_DIR, "aviationstack-mcp", "src")

# Add the src directory directly to Python's path so it can find the module
if AVIATION_SRC_DIR not in sys.path:
    sys.path.append(AVIATION_SRC_DIR)

# MCP Clients 
client = MultiServerMCPClient(
    {
        "tavily":{
            "transport":"streamable_http",
            "url":f"https://mcp.tavily.com/mcp/?tavilyApiKey={TAVILY_API_KEY}"
        },
        
        
        "aviationstack":{
            "transport": "stdio",
            "command": "python",
            "args": [
                "-m",
                "aviationstack_mcp",
                "mcp",
                "run"
            ],
            "env": {
                "AVIATION_STACK_API_KEY": AVIATION_STACK_API_KEY,
                # Explicitly pass the updated PYTHONPATH to the subprocess
                "PYTHONPATH": AVIATION_SRC_DIR
            }
            
            
        },
        
        "weather": {
            "transport": "stdio",
            "command": "python",
            "args": [
                WEATHER_SERVER_PATH
            ],
            "env": {
                "OPENWEATHER_API_KEY": OPENWEATHER_API_KEY
            }
        }
        
    }
    )


# Tools Discovery 
# Cache tools so we don't load them repeatedly
_tools_cache = None

async def get_tools():
    global _tools_cache

    # tools Discovery
    if _tools_cache is None:
        try:
            _tools_cache = await client.get_tools()

        except Exception as e:
            print("\n========== FULL ERROR ==========")
            print(type(e))
            print(repr(e))

            if hasattr(e, "exceptions"):
                print("\nSUB EXCEPTIONS:")
                for i, sub in enumerate(e.exceptions):
                    print(f"\n--- Exception {i+1} ---")
                    print(type(sub))
                    print(repr(sub))

            raise

    return _tools_cache

## Tool Calling
async def call_tool(tool_name: str, args: dict = None):
    # Get Cached Tool
    tools = await get_tools()

    tool = next(
        (tool for tool in tools if tool.name == tool_name),
        None,
    )

    if tool is None:
        raise ValueError(f"Tool '{tool_name}' not found")

    return await tool.ainvoke(args or {})


# ------------------------
#  MCP Tools 
# ------------------------

async def tavily_search(query: str):
    return await call_tool("tavily_search", {"query": query})


async def list_airports(search: str = "", limit: int = 10):
    return await call_tool("list_airports", {"search": search, "limit": limit, "offset": 0})


async def list_airlines(search: str = "", limit: int = 10):
    return await call_tool("list_airlines", {"search": search, "limit": limit, "offset": 0})


async def current_weather(city: str):
    return await call_tool("get_current_weather", {"city": city})


async def forecast(city: str):
    return await call_tool("get_forecast", {"city": city})