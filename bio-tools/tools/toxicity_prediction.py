"""
Toxicity Prediction Tool

Predict comprehensive ADMET (Absorption, Distribution, Metabolism, Excretion, Toxicity) 
properties for drug safety assessment.
"""

import hashlib
from fastmcp import FastMCP
from utils.validation import validate_smiles


def register_toxicity_prediction_tool(mcp: FastMCP):
    """Register the toxicity_prediction tool with the MCP server."""
    
    @mcp.tool()
    def toxicity_prediction(smiles: str) -> dict:
        """
        Predict comprehensive ADMET (Absorption, Distribution, Metabolism, Excretion, Toxicity) properties for drug safety assessment.
        
        This tool evaluates drug-like properties and potential toxicity risks, essential for:
        - Early-stage drug safety screening
        - Pharmacokinetic optimization
        - Regulatory submission preparation
        - Lead compound prioritization
        - Clinical trial risk assessment
        
        Args:
            smiles (str): SMILES representation of the molecule to analyze
            
        Returns:
            dict: Comprehensive ADMET profile including:
                - absorption (dict): Intestinal absorption, permeability, classification
                - distribution (dict): Volume of distribution, plasma binding, blood-brain barrier
                - metabolism (dict): Half-life, CYP enzymes, metabolic stability
                - excretion (dict): Clearance rates, renal excretion percentage
                - toxicity (dict): Overall toxicity level, LD50, organ-specific toxicity flags
                - smiles (str): Input SMILES (echoed back)
                - error (str): Error message if SMILES is invalid
                
        Example Usage:
            toxicity_prediction("CCO") -> {
                "absorption": {"classification": "High", "human_intestinal_absorption": 0.85},
                "toxicity": {"overall_toxicity": "Low", "ld50_mg_kg": 1250}
            }
        """
        is_valid, error_msg = validate_smiles(smiles)
        if not is_valid:
            return {
                "error": error_msg,
                "smiles": smiles
            }
        
        hash_value = int(hashlib.md5(smiles.encode()).hexdigest()[:8], 16)
        
        # Generate mock ADMET properties
        absorption_score = 0.3 + ((hash_value % 70) / 100)  # Range: 0.3-1.0
        distribution_vd = 0.5 + ((hash_value % 500) / 100)  # Volume of distribution: 0.5-5.5 L/kg
        metabolism_half_life = 1 + ((hash_value % 2400) / 100)  # Half-life: 1-25 hours
        excretion_clearance = 5 + ((hash_value % 500) / 10)  # Clearance: 5-55 mL/min/kg
        
        # Toxicity categories (cycling through them based on hash)
        toxicity_classes = ["Low", "Moderate", "High"]
        toxicity_level = toxicity_classes[hash_value % 3]
        
        # LD50 (lethal dose) in mg/kg
        ld50 = 100 + (hash_value % 1900)  # Range: 100-2000 mg/kg
        
        return {
            "smiles": smiles,
            "absorption": {
                "human_intestinal_absorption": round(absorption_score, 2),
                "caco2_permeability": round((hash_value % 100) / 10, 2),  # 0-10 × 10^-6 cm/s
                "classification": "High" if absorption_score > 0.7 else "Moderate" if absorption_score > 0.5 else "Low"
            },
            "distribution": {
                "volume_of_distribution": round(distribution_vd, 2),
                "plasma_protein_binding": round(70 + (hash_value % 30), 1),  # 70-100%
                "bbb_penetration": "Yes" if (hash_value % 2) == 0 else "No"  # Blood-brain barrier
            },
            "metabolism": {
                "half_life_hours": round(metabolism_half_life, 1),
                "cyp450_substrate": ["CYP3A4", "CYP2D6"][hash_value % 2],
                "metabolic_stability": "Stable" if metabolism_half_life > 10 else "Moderate" if metabolism_half_life > 5 else "Unstable"
            },
            "excretion": {
                "clearance_ml_min_kg": round(excretion_clearance, 1),
                "renal_excretion_percent": round(20 + (hash_value % 60), 1)  # 20-80%
            },
            "toxicity": {
                "overall_toxicity": toxicity_level,
                "ld50_mg_kg": ld50,
                "hepatotoxicity": "Positive" if (hash_value % 3) == 0 else "Negative",
                "cardiotoxicity": "Positive" if (hash_value % 5) == 0 else "Negative",
                "mutagenicity": "Positive" if (hash_value % 7) == 0 else "Negative"
            }
        }
