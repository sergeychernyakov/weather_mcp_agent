# Weather MCP Agent (FastAPI + MCP SSE)

This project demonstrates a complete setup of a FastAPI-based MCP (Model Context Protocol) server paired with a FastAgent client using Server-Sent Events (SSE). It provides weather alerts and forecasts via the National Weather Service API.

## Project Structure

```bash
.
├── README.md
├── agent.py                    # FastAgent client entrypoint
├── fastagent.config.yaml       # FastAgent configuration (MCP servers, agent name)
├── fastagent.secrets.yaml      # Secret keys (OpenAI, Anthropic, etc.)
├── pyproject.toml              # Poetry/Setuptools project config & dependencies
├── requirements.txt            # (Optional) pip install list
├── src/
│   ├── __init__.py
│   ├── main.py                 # FastAPI server setup & SSE mount
│   ├── routes.py               # HTTP endpoints: /, /about, /status
│   ├── weather.py              # FastMCP server configuration & @mcp.tool functions
│   └── ...                     # egg-info, pycache, etc.
└── uv.lock                     # Lockfile for `uv` tool
```

## Installing Dependencies

Make sure you have Python 3.12+ and `uv` (the Unicorn/uvicorn wrapper) or `uvicorn` installed:

```bash
# Using `uv`:
uv pip install -r pyproject.toml

# Or directly with pip:
pip install -r requirements.txt
```

If you don't have a `requirements.txt`, install manually:

```bash
pip install fastapi httpx mcp[cli] unicorn fast-agent-mcp
```

## Running the FastAPI MCP Server

Launch the server before starting the agent:

```bash
# Or directly with uvicorn
uvicorn src.main:app --reload
```

The server will expose:
- `GET /`            → HTML welcome page  
- `GET /about`       → Plain text info  
- `GET /status`      → JSON status  
- `POST /messages`   → Internal endpoint for MCP tool calls  
- `GET  /sse`        → SSE endpoint for MCP clients  

## Running the FastAgent Client

The `agent.py` script launches a FastAgent that connects to the MCP server via SSE:

```bash
# Ensure the server is running, then in a new shell:
uv run agent.py        # uses fastagent.config.yaml by default

# Or explicitly:
uv run agent.py -- --debug
```

### Interactive Tool Usage

Once the agent prompt appears:

```text
default >
```

You can invoke your weather tools directly:

```text
# Fetch active alerts for Texas
default > !get_weather_alerts state="TX"

# Fetch a point forecast by coordinates
default > !get_weather_forecast latitude=29.76 longitude=-95.36
```

- The leading `!` tells FastAgent to treat it as a tool call (not an LLM chat).
- `state="TX"` must be in quotes; numeric args can be unquoted.
- Responses from the MCP server will stream back via SSE and print in your console.

## Debugging & Development

- **Inspect tools** locally with MCP Inspector:
  ```bash
  mcp dev ./src/weather.py
  ```
  Opens UI at http://127.0.0.1:6274 and proxies SSE.

- **Agent debug mode**:
  ```bash
  uv run agent.py -- --debug
  ```
  Shows connection logs, SSE events, and tool calls.

## Additional Notes

- Configuration file (`fastagent.config.yaml`) must match agent name and server keys.
- Ensure `weather` MCP server is defined under `mcp:` in the config.
- `fast-agent-mcp` version ≥ 0.2.19 is required for SSE transport.

---

## Author

Sergey Chernyakov
Telegram: @AIBotsTech
