"""
Bio-Tools MCP Server

Exposes biological computation tools via Model Context Protocol:
- molecular_properties: Calculate MW, logP, HBD, HBA from SMILES
- binding_affinity: Predict protein-ligand binding
- toxicity_prediction: Predict ADMET properties
- pubchem_lookup: Search bioactivity data
"""

import os
from dotenv import load_dotenv
from fastmcp import FastMCP
from tools import register_all_tools

load_dotenv()


mcp = FastMCP("bio-tools")
register_all_tools(mcp)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "9000"))
    mcp.run(transport="http", host="127.0.0.1", port=port)
