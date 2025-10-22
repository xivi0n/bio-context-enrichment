"""
SMILES Validation Utilities

This module contains functions for validating SMILES strings and other 
molecular representations used across the bio-tools package.
"""

import re


def validate_smiles(smiles: str) -> tuple[bool, str]:
    """
    Validate SMILES string using regex.
    
    Allowed characters:
    - Letters: C, N, O, S, P, F, Cl, Br, I, B, Si (common atoms)
    - Numbers: 0-9 (atom counts, ring numbers)
    - Symbols: ()[]=#-+@/\\. (bonds, charges, stereochemistry, rings)
    
    Args:
        smiles: SMILES string to validate
        
    Returns:
        tuple: (is_valid: bool, error_message: str)
               If valid: (True, "")
               If invalid: (False, "error description")
    """
    if not smiles or not isinstance(smiles, str):
        return False, "SMILES must be a non-empty string."
    
    # Basic structural checks
    if len(smiles.strip()) == 0:
        return False, "SMILES cannot be empty or whitespace only."
    
    # Simple regex pattern for basic SMILES validation
    # Allows: atoms (C,N,O,S,P,F,Cl,Br,I,B,Si), numbers, bonds, brackets, charges, rings
    smiles_pattern = r'^[CNOSPFBSIcnospfbsilraCH\d\(\)\[\]=#\-\+@/\\.]+$'
    
    # Check if SMILES contains only allowed characters
    if not re.match(smiles_pattern, smiles):
        return False, "SMILES contains invalid characters. Only atoms (C,N,O,S,P,F,Cl,Br,I,B,Si), numbers, and chemical symbols are allowed."
    
    return True, ""
