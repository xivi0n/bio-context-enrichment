"""
Tests for utils.validation module

Tests the SMILES validation functionality used across bio-tools.
"""

import pytest
from utils.validation import validate_smiles


class TestValidateSmiles:
    """Test cases for validate_smiles function."""
    
    def test_valid_simple_smiles(self):
        """Test basic valid SMILES strings."""
        # Simple molecules
        valid, error = validate_smiles("CCO")  # ethanol
        assert valid is True
        assert error == ""
        
        valid, error = validate_smiles("C")  # methane
        assert valid is True
        assert error == ""
        
        valid, error = validate_smiles("CC")  # ethane
        assert valid is True
        assert error == ""
    
    def test_valid_complex_smiles(self):
        """Test more complex valid SMILES strings."""
        # Benzene ring
        valid, error = validate_smiles("C1=CC=CC=C1")
        assert valid is True
        assert error == ""
        
        # Aspirin-like structure
        valid, error = validate_smiles("CC(=O)OC1=CC=CC=C1C(=O)O")
        assert valid is True
        assert error == ""
        
        # With stereochemistry and charges
        valid, error = validate_smiles("C[C@H](N)C(=O)O")
        assert valid is True
        assert error == ""
    
    def test_valid_smiles_with_various_atoms(self):
        """Test SMILES with different allowed atoms."""
        # Common heteroatoms
        valid, error = validate_smiles("CCN")  # with nitrogen
        assert valid is True
        assert error == ""
        
        valid, error = validate_smiles("CCO")  # with oxygen
        assert valid is True
        assert error == ""
        
        valid, error = validate_smiles("CCS")  # with sulfur
        assert valid is True
        assert error == ""
        
        valid, error = validate_smiles("CCP")  # with phosphorus
        assert valid is True
        assert error == ""
        
        valid, error = validate_smiles("CCF")  # with fluorine
        assert valid is True
        assert error == ""
    
    def test_valid_smiles_with_brackets_and_charges(self):
        """Test SMILES with brackets and formal charges."""
        valid, error = validate_smiles("[Na+].[Cl-]")  # salt
        assert valid is True
        assert error == ""
        
        valid, error = validate_smiles("C[N+](C)(C)C")  # quaternary ammonium
        assert valid is True
        assert error == ""
    
    def test_invalid_input_types(self):
        """Test invalid input types."""
        # None input
        valid, error = validate_smiles(None)
        assert valid is False
        assert "non-empty string" in error
        
        # Integer input
        valid, error = validate_smiles(123)
        assert valid is False
        assert "non-empty string" in error
        
        # List input
        valid, error = validate_smiles(["CCO"])
        assert valid is False
        assert "non-empty string" in error
    
    def test_empty_and_whitespace_strings(self):
        """Test empty and whitespace-only strings."""
        # Empty string
        valid, error = validate_smiles("")
        assert valid is False
        assert "non-empty string" in error
        
        # Whitespace only
        valid, error = validate_smiles("   ")
        assert valid is False
        assert "empty or whitespace only" in error
        
        valid, error = validate_smiles("\t\n")
        assert valid is False
        assert "empty or whitespace only" in error
    
    def test_invalid_characters(self):
        """Test SMILES with invalid characters."""
        # Invalid special characters
        valid, error = validate_smiles("CC$O")
        assert valid is False
        assert "invalid characters" in error
        
        valid, error = validate_smiles("CC%O")
        assert valid is False
        assert "invalid characters" in error
        
        valid, error = validate_smiles("CC&O")
        assert valid is False
        assert "invalid characters" in error
        
        # Invalid letters (not allowed atoms)
        valid, error = validate_smiles("CCX")  # X not a standard atom
        assert valid is False
        assert "invalid characters" in error
    
    def test_edge_cases(self):
        """Test edge cases and boundary conditions."""
        # Single atom
        valid, error = validate_smiles("C")
        assert valid is True
        assert error == ""
        
        # Very simple valid molecules
        valid, error = validate_smiles("CC")
        assert valid is True
        assert error == ""
        
        # Numbers (for ring closures)
        valid, error = validate_smiles("C1CC1")
        assert valid is True
        assert error == ""
        
        # Multiple digits
        valid, error = validate_smiles("C12CC1CC2")
        assert valid is True
        assert error == ""
    
    def test_return_type(self):
        """Test that function returns correct types."""
        result = validate_smiles("CCO")
        assert isinstance(result, tuple)
        assert len(result) == 2
        assert isinstance(result[0], bool)
        assert isinstance(result[1], str)
    
    @pytest.mark.parametrize("smiles,expected_valid", [
        ("CCO", True),
        ("C", True),
        ("C1=CC=CC=C1", True),
        ("", False),
        ("CCX", False),
        ("CC$O", False),
        (None, False),
    ])
    def test_parametrized_validation(self, smiles, expected_valid):
        """Parametrized test for various SMILES inputs."""
        valid, error = validate_smiles(smiles)
        assert valid == expected_valid
        if expected_valid:
            assert error == ""
        else:
            assert error != ""
