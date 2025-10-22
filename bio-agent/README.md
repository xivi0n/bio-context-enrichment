# Bio Agent

A Flask-based AI agent for bio-context enrichment that processes natural language prompts using OpenAI's LLM and MCP (Model Context Protocol) tools.

## Features

- **POST /prompt** - Processes prompts using AI routing and reasoning with tool integration
- **GET /health** - Health check endpoint
- **GET /tools** - Lists all available MCP tools
- LLM-powered query routing and tool selection
- Integration with MCP (Model Context Protocol) servers
- Structured logging with timestamps
- Comprehensive error handling

## Prerequisites

### 1. Install uv

Make sure you have [uv](https://docs.astral.sh/uv/) installed. If not, install it:

```bash
# On macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Or with pip
pip install uv
```

### 2. OpenAI API Key (Required)

This project requires an OpenAI API key to function. You'll need to:

1. Get an API key from [OpenAI's website](https://platform.openai.com/api-keys)
2. Set up your environment variables (see Setup section below)

### 3. MCP Server (Optional)

The agent can integrate with MCP (Model Context Protocol) servers for enhanced tool functionality. By default, it will try to connect to `http://localhost:9000/mcp`.

## Setup

### 1. Clone and Navigate

```bash
# Navigate to the bio-agent directory
cd bio-agent
```

### 2. Environment Configuration

Create your environment file from the example:

```bash
# Copy the example environment file
cp .env.example .env
```

Edit the `.env` file and add your OpenAI API key:

```bash
# Bio-Agent Environment Configuration

# OpenAI API Key (REQUIRED)
OPENAI_API_KEY=your_openai_api_key_here

# Flask application port (defaults to 5050)
PORT=5050

# MCP server URL (defaults to http://localhost:9000/mcp)
MCP_URL=http://localhost:9000/mcp
```

### 3. Install Dependencies

```bash
# Sync all dependencies using uv
uv sync
```

### 4. Run the Application

```bash
# Run the application using uv
uv run app.py
```

The server will start on `http://localhost:5050` (or the port specified in your `.env` file)

## API Usage

### Process a Prompt

The main endpoint that processes natural language prompts using AI:

```bash
curl -X POST http://localhost:5050/prompt \
  -H "Content-Type: application/json" \
  -d '{"prompt": "What is the molecular weight of aspirin?"}'
```

**Response Format:**

```json
{
  "status": "success",
  "prompt": "What is the molecular weight of aspirin?",
  "decision": {
    "needs_tools": true,
    "required_tools": [...],
    "reasoning": "..."
  },
  "tool_results": [...],
  "response": {
    "rationale": "...",
    "result": "..."
  }
}
```

### List Available Tools

Get a list of all MCP tools available to the agent:

```bash
curl http://localhost:5050/tools
```

## How It Works

1. **Prompt Reception**: The `/prompt` endpoint receives natural language queries
2. **AI Router**: Uses OpenAI's LLM to analyze the prompt and decide if tools are needed
3. **Tool Execution**: If tools are required, executes the appropriate MCP tools
4. **AI Reasoner**: Uses the LLM again to generate a comprehensive response based on tool results
5. **Response**: Returns structured JSON with the decision process, tool results, and final answer

## Architecture

```
User Prompt → Router (LLM) → Tool Selection (Optional) → Tool Execution → Reasoner (LLM) → Response
```

- **Router**: Analyzes prompts to determine tool requirements
- **Tools Service**: Manages MCP client connections and tool execution
- **Reasoner**: Synthesizes tool results into coherent responses
- **LLM Service**: Handles OpenAI API interactions

## Development

### Testing

The project includes comprehensive test coverage for all major components:

```bash
# Run all tests
uv run pytest

# Run tests with verbose output
uv run pytest -v

# Run tests with coverage report
uv run pytest --cov
```

**Test Structure:**

- `tests/test_app.py` - Flask endpoint tests (health, tools, prompt endpoints)
- `tests/test_llm_service.py` - LLM service unit tests (router, reasoner functions)
- `tests/conftest.py` - Test fixtures and configuration

All tests use mocking to avoid external API calls during testing.

### Code Quality Tools

```bash
# Format code with black
uv run black .

# Lint code with flake8
uv run flake8 .
```

## Dependencies

### Core Dependencies

- **Flask 2.3.3** - Web framework for the API server
- **OpenAI ≥1.0.0** - OpenAI API client for LLM interactions
- **fastmcp ≥0.1.0** - Model Context Protocol client
- **python-dotenv ≥1.0.0** - Environment variable management
- **requests 2.31.0** - HTTP client library

### Development Dependencies

- **pytest ≥7.0.0** - Testing framework
- **pytest-cov ≥4.0.0** - Test coverage reporting
- **black ≥22.0.0** - Code formatter
- **flake8 ≥5.0.0** - Code linter

All dependencies are automatically managed and synced with `uv sync`

## Troubleshooting

### Common Issues

**1. "OPENAI_API_KEY not found in environment variables"**

- Ensure you've created a `.env` file from `.env.example`
- Verify your OpenAI API key is correctly set in the `.env` file
- Make sure there are no extra spaces or quotes around the key

**2. MCP Connection Issues**

- The MCP server connection is optional - the agent will work without it
- Check if your MCP server is running on the configured URL
- Verify the `MCP_URL` in your `.env` file is correct

**3. Port Already in Use**

- Change the `PORT` in your `.env` file to a different value
- Or kill any existing process using the port: `lsof -ti:5050 | xargs kill -9`

**4. Import/Dependency Errors**

- Run `uv sync` to ensure all dependencies are installed
- Try deleting `uv.lock` and running `uv sync` again

### Alternative Setup (Traditional Method)

If you prefer to use a traditional virtual environment:

```bash
# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # On macOS/Linux
# .venv\Scripts\activate  # On Windows

# Install dependencies
pip install -e .

# Run the application
python app.py
```
