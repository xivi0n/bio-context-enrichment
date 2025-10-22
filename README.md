# Bio Context Enrichment

An AI agent that enriches its context by calling in-silico biological tools, then uses that enriched context to make informed decisions about molecular queries.

## Architecture

The system consists of three components:

1. **bio-tools** - MCP server exposing biological computation tools
2. **bio-agent** - Flask API that routes queries and integrates with bio-tools
3. **bio-ui** - Vue.js interface demonstrating the enrichment pipeline

## Components

### bio-tools (MCP Server)

Exposes 4 biological computation tools via Model Context Protocol:

- **molecular_properties**: Calculate MW, logP, HBD, HBA from SMILES
- **binding_affinity**: Predict protein-ligand binding affinity
- **toxicity_prediction**: Predict ADMET properties
- **pubchem_lookup**: Search bioactivity data

```bash
cd bio-tools
uv sync
uv run server.py
# Server runs on http for MCP communication on http://localhost:9000
```

### bio-agent (Flask API)

AI agent with LLM-powered routing and reasoning:

- **POST /prompt** - Process natural language queries using bio-tools
- **GET /health** - Health check
- **GET /tools** - List available MCP tools

Requires OpenAI API key in environment.

```bash
cd bio-agent
uv sync
export OPENAI_API_KEY=your_key_here
uv run app.py
# Server runs on http://localhost:5050
```

### bio-ui (Vue Interface)

Interactive demonstration of the 3-step enrichment pipeline:

1. Query Understanding (classification + entity extraction)
2. Context Enrichment (tool calls + aggregation)
3. Reasoning + Rationale (final decision with explanations)

```bash
cd bio-ui
npm install
npm run dev
# Server runs on http://localhost:5173
```

## Testing

```bash
# Test bio-tools
cd bio-tools && uv run pytest

# Test bio-agent
cd bio-agent && uv run pytest

# No tests for bio-ui (demonstration only)
```
