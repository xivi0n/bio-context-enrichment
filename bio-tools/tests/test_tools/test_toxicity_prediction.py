"""
Tests for tools.toxicity_prediction module

Tests the toxicity prediction functionality.
"""

import pytest
from unittest.mock import MagicMock
from fastmcp import FastMCP
from tools.toxicity_prediction import register_toxicity_prediction_tool


class TestToxicityPredictionTool:
    """Test cases for toxicity prediction tool."""
    
    def setup_method(self):
        """Set up test fixtures before each test method."""
        self.mcp = MagicMock(spec=FastMCP)
        self.tool_func = None
        
        # Capture the registered tool function
        def mock_tool(func):
            self.tool_func = func
            return func
        
        self.mcp.tool.return_value = mock_tool
        register_toxicity_prediction_tool(self.mcp)
    
    def test_tool_registration(self):
        """Test that the tool is properly registered with MCP."""
        assert self.mcp.tool.called
        assert self.tool_func is not None
        assert self.tool_func.__name__ == "toxicity_prediction"
    
    def test_valid_smiles_prediction(self):
        """Test toxicity prediction with valid SMILES."""
        result = self.tool_func("CCO")
        
        assert "error" not in result
        assert result["smiles"] == "CCO"
        assert "absorption" in result
        assert "distribution" in result
        assert "metabolism" in result
        assert "excretion" in result
        assert "toxicity" in result
        
        # Check that each section contains expected data
        assert isinstance(result["absorption"], dict)
        assert isinstance(result["distribution"], dict)
        assert isinstance(result["metabolism"], dict)
        assert isinstance(result["excretion"], dict)
        assert isinstance(result["toxicity"], dict)
    
    def test_invalid_smiles(self):
        """Test behavior with invalid SMILES."""
        result = self.tool_func("")
        
        assert "error" in result
        assert result["smiles"] == ""
        assert "absorption" not in result
    
    def test_deterministic_results(self):
        """Test that results are deterministic for same input."""
        result1 = self.tool_func("CCO")
        result2 = self.tool_func("CCO")
        
        assert result1 == result2
    
    def test_different_smiles_different_results(self):
        """Test that different SMILES produce different results."""
        result1 = self.tool_func("CCO")
        result2 = self.tool_func("CCC")
        
        # Different SMILES should give different results
        assert result1 != result2
    
    @pytest.mark.parametrize("smiles", [
        "CCO",
        "C",
        "CC",
        "C1=CC=CC=C1",
    ])
    def test_various_valid_smiles(self, smiles):
        """Test various valid SMILES strings."""
        result = self.tool_func(smiles)
        
        assert "error" not in result
        assert result["smiles"] == smiles
        assert all(section in result for section in ["absorption", "distribution", "metabolism", "excretion", "toxicity"])
