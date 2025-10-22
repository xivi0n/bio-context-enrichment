# Bio-Tools MCP Server

A Model Context Protocol (MCP) server that exposes biological computation tools for molecular analysis and drug discovery.

## Tools

### 1. molecular_properties

Calculate molecular properties from SMILES strings.

**Parameters:**

- `smiles` (str): SMILES representation of the molecule

**Returns:**

- `molecular_weight`: Molecular weight in g/mol
- `logP`: Partition coefficient (lipophilicity)
- `hbd`: Hydrogen bond donors count
- `hba`: Hydrogen bond acceptors count

### 2. binding_affinity

Predict protein-ligand binding affinity.

**Parameters:**

- `protein_id` (str): Protein identifier (UniProt ID or PDB ID)
- `ligand_smiles` (str): SMILES representation of the ligand

**Returns:**

- `binding_affinity`: Predicted binding affinity (kcal/mol)
- `confidence`: Prediction confidence score (0-1)
- `pose`: Predicted binding pose information

### 3. toxicity_prediction

Predict ADMET (Absorption, Distribution, Metabolism, Excretion, Toxicity) properties.

**Parameters:**

- `smiles` (str): SMILES representation of the molecule

**Returns:**

- `absorption`: Absorption prediction
- `distribution`: Distribution prediction
- `metabolism`: Metabolism prediction
- `excretion`: Excretion prediction
- `toxicity`: Toxicity prediction

### 4. pubchem_lookup

Search PubChem for bioactivity data.

**Parameters:**

- `query` (str): Search query (compound name, CID, SMILES, etc.)
- `search_type` (str, optional): Type of search - "compound", "assay", or "bioactivity" (default: "compound")

**Returns:**

- `results`: List of matching compounds/assays
- `bioactivity_data`: Associated bioactivity information
- `count`: Number of results found

## Installation & Running

### Option 1: Using uv (Recommended)

The easiest way to run the server is using [uv](https://docs.astral.sh/uv/), which handles dependencies automatically:

```bash
# Install uv if not already installed
curl -LsSf https://astral.sh/uv/install.sh | sh

# Navigate to the project directory
cd bio-tools

# Install dependencies (creates virtual environment automatically)
uv sync

# Run the server
uv run server.py
```

**Alternative: Run directly without explicit sync**

```bash
# uv run automatically installs dependencies from pyproject.toml
uv run server.py

# Or from any directory with full path
uv run --project /path/to/bio-tools /path/to/bio-tools/server.py
```

**Managing dependencies with uv:**

```bash
# Add a new dependency
uv add package-name

# Add development dependency
uv add --dev pytest

# Install from requirements file
uv pip install -r requirements.txt

# Show installed packages
uv pip list
```

### Option 2: Traditional Python Virtual Environment

```bash
cd bio-tools
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

**Running the Server:**

```bash
python server.py
```

Or using FastMCP's CLI:

```bash
fastmcp run server.py
```

## Testing

The project includes comprehensive tests for all tools and utilities.

### Running Tests with uv (Recommended)

```bash
# Run all tests
uv run pytest tests/

# Run tests with verbose output
uv run pytest tests/ -v

# Run tests with coverage report
uv run pytest tests/ --cov=tools --cov=utils

# Run tests with detailed coverage (shows missing lines)
uv run pytest tests/ --cov=tools --cov=utils --cov-report=term-missing

# Run only specific test files
uv run pytest tests/test_utils/test_validation.py
uv run pytest tests/test_tools/test_binding_affinity.py

# Run tests matching a pattern
uv run pytest tests/ -k "validation"
```

### Running Tests with Traditional Setup

```bash
# First activate your virtual environment
source .venv/bin/activate

# Install test dependencies
pip install pytest pytest-cov

# Run tests
pytest tests/
```

### Test Structure

- `tests/test_utils/` - Tests for utility functions (validation, etc.)
- `tests/test_tools/` - Tests for all bio-tools (binding affinity, molecular properties, etc.)
- Tests cover input validation, error handling, deterministic results, and proper return types

## Development

The tools currently return mock data.

## Integration with MCP Clients

This server can be used with any MCP-compatible client. Configure your client to connect to this server to access the biological computation tools.
