"""
Tests for tools.pubchem_lookup module

Tests the PubChem database lookup functionality.
"""

import pytest
from unittest.mock import MagicMock
from fastmcp import FastMCP
from tools.pubchem_lookup import register_pubchem_lookup_tool


class TestPubChemLookupTool:
    """Test cases for PubChem lookup tool."""
    
    def setup_method(self):
        """Set up test fixtures before each test method."""
        self.mcp = MagicMock(spec=FastMCP)
        self.tool_func = None
        
        # Capture the registered tool function
        def mock_tool(func):
            self.tool_func = func
            return func
        
        self.mcp.tool.return_value = mock_tool
        register_pubchem_lookup_tool(self.mcp)
    
    def test_tool_registration(self):
        """Test that the tool is properly registered with MCP."""
        assert self.mcp.tool.called
        assert self.tool_func is not None
        assert self.tool_func.__name__ == "pubchem_lookup"
    
    def test_compound_search_default(self):
        """Test compound search with default search type."""
        result = self.tool_func("aspirin")
        
        assert "results" in result
        assert "count" in result
        assert isinstance(result["results"], list)
        assert isinstance(result["count"], int)
        assert result["count"] >= 0
    
    def test_compound_search_explicit(self):
        """Test explicit compound search."""
        result = self.tool_func("CCO", "compound")
        
        assert "results" in result
        assert "count" in result
        assert isinstance(result["results"], list)
    
    def test_assay_search(self):
        """Test assay search type."""
        result = self.tool_func("EGFR", "assay")
        
        assert "results" in result
        assert "count" in result
        assert isinstance(result["results"], list)
    
    def test_bioactivity_search(self):
        """Test bioactivity search type."""
        result = self.tool_func("kinase", "bioactivity")
        
        assert "results" in result
        assert "summary" in result
        assert "count" in result
        assert isinstance(result["results"], list)
        assert isinstance(result["summary"], dict)
    
    def test_deterministic_results(self):
        """Test that results are deterministic for same input."""
        result1 = self.tool_func("aspirin", "compound")
        result2 = self.tool_func("aspirin", "compound")
        
        assert result1 == result2
    
    def test_different_queries_different_results(self):
        """Test that different queries produce different results."""
        result1 = self.tool_func("aspirin", "compound")
        result2 = self.tool_func("ibuprofen", "compound")
        
        # Different queries should give different results
        assert result1 != result2
    
    def test_different_search_types_different_results(self):
        """Test that different search types produce different results."""
        result1 = self.tool_func("kinase", "compound")
        result2 = self.tool_func("kinase", "assay")
        result3 = self.tool_func("kinase", "bioactivity")
        
        # Different search types should give different structures
        assert result1 != result2
        assert result2 != result3
        
        # But all should have basic structure
        for result in [result1, result2, result3]:
            assert "results" in result
            assert "count" in result
    
    @pytest.mark.parametrize("search_type", ["compound", "assay", "bioactivity"])
    def test_all_search_types(self, search_type):
        """Test all supported search types."""
        result = self.tool_func("test_query", search_type)
        
        assert "results" in result
        assert "count" in result
        assert isinstance(result["results"], list)
        assert isinstance(result["count"], int)
    
    def test_empty_query(self):
        """Test behavior with empty query."""
        result = self.tool_func("", "compound")
        
        # Should still return valid structure even for empty query
        assert "results" in result
        assert "count" in result
    
    @pytest.mark.parametrize("query", [
        "aspirin",
        "2244",  # CID
        "CC(=O)OC1=CC=CC=C1C(=O)O",  # SMILES
        "EGFR inhibitor",
    ])
    def test_various_query_types(self, query):
        """Test various query types mentioned in docstring."""
        result = self.tool_func(query, "compound")
        
        assert "results" in result
        assert "count" in result
