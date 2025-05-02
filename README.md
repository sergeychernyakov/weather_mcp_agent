# Weather MCP Agent (FastAPI + MCP SSE)

This project demonstrates a complete setup of a FastAPI-based MCP (Model Context Protocol) server paired with a FastAgent client using Server-Sent Events (SSE). It provides weather alerts and forecasts via the National Weather Service API.

## Project Structure

```bash
.
├── README.md
├── agent.py                    # FastAgent client entrypoint
├── fastagent.config.yaml       # FastAgent configuration (MCP servers, agent name)
├── fastagent.secrets.yaml      # Secret keys (OpenAI, Anthropic, etc.)
├── pyproject.toml              # Project dependencies (setuptools/poetry)
├── requirements.txt            # (Optional) pip install list
├── src/
│   ├── __init__.py
│   ├── main.py                 # FastAPI server setup & SSE mount
│   ├── routes.py               # HTTP endpoints: /, /about, /status
│   ├── weather.py              # FastMCP server config & @mcp.tool functions
│   └── ...                     # egg-info, pycache, etc.
└── uv.lock                     # Lockfile for `uv` tool
```

---

### 1. Clone the Repository

Begin by cloning the repository to your local machine:

```bash
git clone git@github.com:sergeychernyakov/weather_mcp_agent.git
cd weather_mcp_agent
```

### 2. Create a Virtual Environment

It's recommended to use a virtual environment to manage dependencies:

```bash
python3 -m venv .venv
```

### 3. Activate the Virtual Environment

Activate the virtual environment before installing dependencies.

- **Linux/MacOS:**

    ```bash
    source .venv/bin/activate
    ```

- **Windows:**

    ```bash
    .venv\Scripts\activate
    ```

## Installing Dependencies

Requires **Python 3.12+** and [uv](https://github.com/astral-sh/uv) or `uvicorn`.

```bash
# Using uv:
uv pip install -r pyproject.toml

# Or directly with pip:
pip install -r requirements.txt
```

If you don’t have a `requirements.txt`, install manually:

```bash
pip install fastapi httpx mcp[cli] unicorn fast-agent-mcp
```

---

## Running the FastAPI MCP Server

Launch the server before starting the agent:

```bash
uvicorn src.main:app --reload
```

The server exposes:
- `GET /` → HTML welcome page
- `GET /about` → Plain text info
- `GET /status` → JSON status
- `POST /messages` → Internal endpoint for MCP tool calls
- `GET /sse` → SSE endpoint for MCP clients

---

## Running the FastAgent Client

The `agent.py` script launches a FastAgent that connects to the MCP server via SSE:

```bash
# Ensure the server is running, then in a new shell:
uv run agent.py        # uses fastagent.config.yaml by default

# Or explicitly:
uv run agent.py -- --debug
```

---

## Interactive Tool Usage

Once the agent prompt appears:

```
default >
```

You can invoke your weather tools directly:

```bash
# Fetch active alerts for Texas
!get_weather_alerts state="TX"

# Fetch a point forecast by coordinates
!get_weather_forecast latitude=29.76 longitude=-95.36
```

- The leading `!` tells FastAgent to treat it as a tool call (not a chat).
- `state="TX"` must be in quotes; numeric args can be unquoted.
- Responses from the MCP server will stream back via SSE and print in your console.

---

## Debugging & Development

- Inspect tools locally with MCP Inspector:

```bash
mcp dev ./src/weather.py
```
Opens UI at http://127.0.0.1:6274 and proxies SSE.

- Agent debug mode:
```bash
uv run agent.py -- --debug
```
Shows connection logs, SSE events, and tool calls.

---

## 🧑‍💻 Using with ChatGPT Assistants

You have two main options to let ChatGPT talk to your weather tools:

### 1. ChatGPT Plugin via OpenAPI

1. **Create a plugin manifest file** `ai-plugin.json` in your project root:

```json
{
  "schema_version": "v1",
  "name_for_human": "Weather MCP Agent",
  "name_for_model": "weather_agent",
  "description_for_human": "Get weather alerts & forecasts",
  "description_for_model": "Plugin for fetching weather alerts and forecasts via SSE.",
  "auth": { "type": "none" },
  "api": {
    "type": "openapi",
    "url": "http://localhost:8000/openapi.json",
    "is_user_authenticated": false
  },
  "logo_url": "http://localhost:8000/logo.png",
  "contact_email": "you@example.com",
  "legal_info_url": "http://example.com/legal"
}
```

2. **Serve that file** (and your OpenAPI spec) by mounting the `.well-known` folder in `src/main.py`:

```python
from fastapi.staticfiles import StaticFiles

app.mount("/.well-known", StaticFiles(directory="."), name="well-known")
```

Now available at:
- http://localhost:8000/.well-known/ai-plugin.json
- http://localhost:8000/openapi.json

3. **Expose your server publicly** (reverse proxy, or `ngrok http 8000`) so ChatGPT can reach it.
4. **In ChatGPT UI**: Plugins → Develop your own → From URL, and enter:

```
https://<your-domain>/.well-known/ai-plugin.json
```

Activate the plugin, then ask:
> What are the active weather alerts in Texas?

ChatGPT will discover `get_weather_alerts(state: string)` and call it.

---

### 2. Function-Calling with the OpenAI API

If you’re writing your own ChatGPT-style client, just pass the OpenAPI schema to the `ChatCompletion.create()` call:

```python
import openai
import json

with open("openapi.json") as f:
    spec = json.load(f)

response = openai.ChatCompletion.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": "Show me weather alerts for CA"}],
    functions=spec["paths"],
    function_call="auto",
)
```

The model will then invoke your `/messages` → `/sse` pipeline under the hood and return the tool’s JSON response.

---

## Additional Notes

- The configuration file (`fastagent.config.yaml`) must match agent name and server keys.
- Ensure the `weather` MCP server is defined under `mcp:` in the config.
- `fast-agent-mcp` version **≥ 0.2.19** is required for SSE transport.

---

## Author

**Sergey Chernyakov**  
📬 Telegram: [@AIBotsTech](https://t.me/AIBotsTech)
