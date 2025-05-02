# agent.py

"""
Weather FastAgent – MCP-native agent that exposes the tools defined in
`weather.py`.

Run it interactively for dev / debugging:

    mcp dev ./src/agent.py

Or just start it as a server:

    python src/agent.py                 # SSE transport on :8000
    uv run src/agent.py -- --port 8088  # override defaults with CLI flags

Dependencies
------------
`FastAgent` lives in the **fast-agent** package which is *not* part of
`mcp-agent`.  Install it once:

    pip install fast-agent-mcp
"""

from __future__ import annotations
import asyncio
from mcp_agent.core.fastagent import FastAgent

# --------------------------------------------------------------------------- #
# Build the agent
# --------------------------------------------------------------------------- #
fast = FastAgent("weather-agent")

@fast.agent(instruction="You are a cheerful weather assistant 🌤️.", servers=["weather"])
async def main() -> None:
    """
    Interactive entry-point registered with FastAgent.

    When you execute `python src/agent.py`, FastAgent parses its own CLI flags
    automatically – try `python src/agent.py --help` for the full list.
    """
    async with fast.run() as agent:
        # response = await agent('!get_weather_alerts state="FL"')
        # print("MCP Server Response:", response)

        # Drop the user into an interactive REPL (supports MCP tool calls).
        await agent.interactive()

# --------------------------------------------------------------------------- #
# Script entry-point
# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    asyncio.run(main())
