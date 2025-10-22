"""
Bio-Tools Package

This package contains all the biological computation tools exposed via MCP.
Each tool is implemented in a separate module for better organization and maintainability.
"""

from fastmcp import FastMCP
from .molecular_properties import register_molecular_properties_tool
from .binding_affinity import register_binding_affinity_tool
from .toxicity_prediction import register_toxicity_prediction_tool
from .pubchem_lookup import register_pubchem_lookup_tool


def register_all_tools(mcp: FastMCP):
    """Register all bio-tools with the MCP server."""
    register_molecular_properties_tool(mcp)
    register_binding_affinity_tool(mcp)
    register_toxicity_prediction_tool(mcp)
    register_pubchem_lookup_tool(mcp)
