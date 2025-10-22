"""
Tests for tools.binding_affinity module

Tests the binding affinity prediction functionality.
"""

import pytest
from unittest.mock import MagicMock
from fastmcp import FastMCP
from tools.binding_affinity import register_binding_affinity_tool


class TestBindingAffinityTool:
    """Test cases for binding affinity tool."""
    
    def setup_method(self):
        """Set up test fixtures before each test method."""
        self.mcp = MagicMock(spec=FastMCP)
        self.tool_func = None
        
        # Capture the registered tool function
        def mock_tool(func):
            self.tool_func = func
            return func
        
        self.mcp.tool.return_value = mock_tool
        register_binding_affinity_tool(self.mcp)
    
    def test_tool_registration(self):
        """Test that the tool is properly registered with MCP."""
        assert self.mcp.tool.called
        assert self.tool_func is not None
        assert self.tool_func.__name__ == "binding_affinity"
    
    def test_valid_smiles_default_target(self):
        """Test binding affinity prediction with valid SMILES and default target."""
        result = self.tool_func("CCO")
        
        assert "error" not in result
        assert result["target"] == "EGFR"
        assert result["smiles"] == "CCO"
        assert "binding_affinity_kcal_mol" in result
        assert "pKd" in result
        assert "confidence" in result
        
        # Check value ranges
        assert -15 <= result["binding_affinity_kcal_mol"] <= -3
        assert 4.0 <= result["pKd"] <= 9.0
        assert 0.2 <= result["confidence"] <= 0.99
    
    def test_valid_smiles_custom_target(self):
        """Test binding affinity prediction with custom target."""
        result = self.tool_func("CC(=O)OC1=CC=CC=C1C(=O)O", "CDK2")
        
        assert "error" not in result
        assert result["target"] == "CDK2"
        assert result["smiles"] == "CC(=O)OC1=CC=CC=C1C(=O)O"
        assert "binding_affinity_kcal_mol" in result
        assert "pKd" in result
        assert "confidence" in result
    
    def test_invalid_smiles(self):
        """Test behavior with invalid SMILES."""
        result = self.tool_func("", "EGFR")
        
        assert "error" in result
        assert result["smiles"] == ""
        assert result["target"] == "EGFR"
        assert "binding_affinity_kcal_mol" not in result
    
    def test_invalid_smiles_with_bad_characters(self):
        """Test behavior with SMILES containing invalid characters."""
        result = self.tool_func("CC$O", "EGFR")
        
        assert "error" in result
        assert "invalid characters" in result["error"]
        assert result["smiles"] == "CC$O"
        assert result["target"] == "EGFR"
    
    def test_deterministic_results(self):
        """Test that results are deterministic for same input."""
        result1 = self.tool_func("CCO", "EGFR")
        result2 = self.tool_func("CCO", "EGFR")
        
        assert result1 == result2
    
    def test_different_inputs_different_results(self):
        """Test that different inputs produce different results."""
        result1 = self.tool_func("CCO", "EGFR")
        result2 = self.tool_func("CCC", "EGFR")
        result3 = self.tool_func("CCO", "CDK2")
        
        # Different SMILES should give different results
        assert result1 != result2
        
        # Different targets should give different results
        assert result1 != result3
    
    def test_result_types(self):
        """Test that result values have correct types."""
        result = self.tool_func("CCO", "EGFR")
        
        assert isinstance(result["target"], str)
        assert isinstance(result["smiles"], str)
        assert isinstance(result["binding_affinity_kcal_mol"], (int, float))
        assert isinstance(result["pKd"], (int, float))
        assert isinstance(result["confidence"], (int, float))

    
    @pytest.mark.parametrize("smiles,target", [
        ("CCO", "EGFR"),
        ("C", "CDK2"),
        ("C1=CC=CC=C1", "VEGFR2"),
        ("CC(=O)OC1=CC=CC=C1C(=O)O", "p53"),
    ])
    def test_various_valid_inputs(self, smiles, target):
        """Test various combinations of valid SMILES and targets."""
        result = self.tool_func(smiles, target)
        
        assert "error" not in result
        assert result["target"] == target
        assert result["smiles"] == smiles
        assert -15 <= result["binding_affinity_kcal_mol"] <= -3
        assert 4.0 <= result["pKd"] <= 9.0
        assert 0.2 <= result["confidence"] <= 0.99
    
    def test_common_targets(self):
        """Test with commonly used protein targets mentioned in docstring."""
        targets = ["EGFR", "VEGFR2", "CDK2", "p53", "BRAF", "ALK", "HER2", "PI3K"]
        
        for target in targets:
            result = self.tool_func("CCO", target)
            assert "error" not in result
            assert result["target"] == target
