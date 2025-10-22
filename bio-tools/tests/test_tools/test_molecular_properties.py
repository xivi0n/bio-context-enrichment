"""
Tests for tools.molecular_properties module

Tests the molecular properties calculation functionality.
"""

import pytest
from unittest.mock import MagicMock
from fastmcp import FastMCP
from tools.molecular_properties import register_molecular_properties_tool


class TestMolecularPropertiesTool:
    """Test cases for molecular properties tool."""
    
    def setup_method(self):
        """Set up test fixtures before each test method."""
        self.mcp = MagicMock(spec=FastMCP)
        self.tool_func = None
        
        # Capture the registered tool function
        def mock_tool(func):
            self.tool_func = func
            return func
        
        self.mcp.tool.return_value = mock_tool
        register_molecular_properties_tool(self.mcp)
    
    def test_tool_registration(self):
        """Test that the tool is properly registered with MCP."""
        assert self.mcp.tool.called
        assert self.tool_func is not None
        assert self.tool_func.__name__ == "molecular_properties"
    
    def test_valid_smiles_properties(self):
        """Test molecular properties calculation with valid SMILES."""
        result = self.tool_func("CCO")
        
        assert "error" not in result
        assert result["smiles"] == "CCO"
        assert "molecular_weight" in result
        assert "logP" in result
        assert "hbd" in result
        assert "hba" in result
        
        # Check value ranges
        assert 200 <= result["molecular_weight"] <= 500
        assert -2 <= result["logP"] <= 8
        assert 0 <= result["hbd"] <= 7
        assert 0 <= result["hba"] <= 11
    
    def test_complex_smiles_properties(self):
        """Test with more complex SMILES."""
        result = self.tool_func("CC(=O)OC1=CC=CC=C1C(=O)O")  # aspirin-like
        
        assert "error" not in result
        assert result["smiles"] == "CC(=O)OC1=CC=CC=C1C(=O)O"
        assert all(key in result for key in ["molecular_weight", "logP", "hbd", "hba"])
    
    def test_invalid_smiles(self):
        """Test behavior with invalid SMILES."""
        result = self.tool_func("")
        
        assert "error" in result
        assert result["smiles"] == ""
        assert "molecular_weight" not in result
    
    def test_invalid_smiles_with_bad_characters(self):
        """Test behavior with SMILES containing invalid characters."""
        result = self.tool_func("CC$O")
        
        assert "error" in result
        assert "invalid characters" in result["error"]
        assert result["smiles"] == "CC$O"
    
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
    
    def test_result_types(self):
        """Test that result values have correct types."""
        result = self.tool_func("CCO")
        
        assert isinstance(result["smiles"], str)
        assert isinstance(result["molecular_weight"], (int, float))
        assert isinstance(result["logP"], (int, float))
        assert isinstance(result["hbd"], int)
        assert isinstance(result["hba"], int)
    
    def test_integer_properties_ranges(self):
        """Test that integer properties are within expected ranges."""
        # Test multiple SMILES to check range validity
        test_smiles = ["CCO", "C", "CC", "CCC", "CCCC", "C1=CC=CC=C1"]
        
        for smiles in test_smiles:
            result = self.tool_func(smiles)
            if "error" not in result:
                assert 0 <= result["hbd"] <= 7
                assert 0 <= result["hba"] <= 11
    
    @pytest.mark.parametrize("smiles", [
        "CCO",
        "C",
        "CC",
        "C1=CC=CC=C1",
        "CC(=O)OC1=CC=CC=C1C(=O)O",
        "CCN",
        "CCS",
        "CCP",
    ])
    def test_various_valid_smiles(self, smiles):
        """Test various valid SMILES strings."""
        result = self.tool_func(smiles)
        
        assert "error" not in result
        assert result["smiles"] == smiles
        assert 200 <= result["molecular_weight"] <= 500
        assert -2 <= result["logP"] <= 8
        assert 0 <= result["hbd"] <= 7
        assert 0 <= result["hba"] <= 11
    
    def test_lipinski_rule_related_properties(self):
        """Test that properties are suitable for drug-likeness assessment."""
        result = self.tool_func("CCO")
        
        # Properties should be in ranges that make sense for Lipinski's Rule of Five
        assert "error" not in result
        
        # Molecular weight should be reasonable for drug-like molecules
        assert result["molecular_weight"] > 0
        
        # logP should be in a reasonable range for drug-like molecules
        assert result["logP"] >= -2
        
        # HBD and HBA counts should be reasonable
        assert result["hbd"] >= 0
        assert result["hba"] >= 0
