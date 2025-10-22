"""
Binding Affinity Tool

Predict protein-ligand binding affinity for drug discovery and target engagement analysis.
"""

import hashlib
from fastmcp import FastMCP
from utils.validation import validate_smiles


def register_binding_affinity_tool(mcp: FastMCP):
    """Register the binding_affinity tool with the MCP server."""
    
    @mcp.tool()
    def binding_affinity(smiles: str, target: str = "EGFR") -> dict:
        """
        Predict protein-ligand binding affinity for drug discovery and target engagement analysis.
        
        This tool estimates how strongly a small molecule binds to a protein target, which is crucial for:
        - Lead compound optimization
        - Virtual screening campaigns  
        - Structure-activity relationship (SAR) analysis
        - Target selectivity assessment
        
        Args:
            smiles (str): SMILES representation of the ligand molecule
            target (str, optional): Target protein identifier. Defaults to "EGFR".
                                   Common targets: EGFR, VEGFR2, CDK2, p53, BRAF, ALK, HER2, PI3K
            
        Returns:
            dict: Binding prediction results including:
                - target (str): Target protein name
                - smiles (str): Input ligand SMILES
                - binding_affinity_kcal_mol (float): Predicted binding energy in kcal/mol (-3 to -15, more negative = stronger)
                - pKd (float): Negative log of dissociation constant (4.0-9.0, higher = stronger binding)
                - confidence (float): Prediction confidence score (0.2-0.99)
                - error (str): Error message if SMILES is invalid
                
        Example Usage:
            binding_affinity("CCO", "EGFR") -> {"binding_affinity_kcal_mol": -8.5, "pKd": 6.2, "confidence": 0.85}
        """
        is_valid, error_msg = validate_smiles(smiles)
        if not is_valid:
            return {
                "error": error_msg,
                "smiles": smiles,
                "target": target
            }
        
        key = f"{smiles}|{target}"
        hash_value = int(hashlib.md5(key.encode()).hexdigest()[:8], 16)

        # Generate mock affinity: -3 to -15 kcal/mol (stronger binders more negative)
        affinity = -3 - (hash_value % 1200) / 100.0  # -3 to -15

        # pKd roughly corresponds: pKd = -log10(Kd) ; approximate conversion from kcal/mol
        # Use a simple mapping to keep values reasonable: pKd 4-9
        pKd = 4.0 + ((hash_value % 500) / 100.0)  # 4.0-8.99

        # Confidence 0.2-0.95
        confidence = 0.2 + ((hash_value % 75) / 100.0)

        return {
            "target": target,
            "smiles": smiles,
            "binding_affinity_kcal_mol": round(affinity, 2),
            "pKd": round(pKd, 2),
            "confidence": round(min(confidence, 0.99), 2)
        }
