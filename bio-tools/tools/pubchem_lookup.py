"""
PubChem Lookup Tool

Search PubChem database for chemical compounds, biological assays, and bioactivity data.
"""

import hashlib
from fastmcp import FastMCP


def register_pubchem_lookup_tool(mcp: FastMCP):
    """Register the pubchem_lookup tool with the MCP server."""
    
    @mcp.tool()
    def pubchem_lookup(query: str, search_type: str = "compound") -> dict:
        """
        Search PubChem database for chemical compounds, biological assays, and bioactivity data.
        
        PubChem is the world's largest collection of freely accessible chemical information, containing
        millions of chemical structures and their associated biological activities. This tool provides:
        - Chemical compound discovery and property lookup
        - Biological assay identification and metadata
        - Bioactivity data mining for drug discovery
        - Structure-activity relationship analysis
        - Literature-derived experimental data
        
        Args:
            query (str): Search query - can be compound name, CID, SMILES, target protein, or keyword
                        Examples: "aspirin", "2244" (CID), "CC(=O)OC1=CC=CC=C1C(=O)O", "EGFR inhibitor"
            search_type (str, optional): Type of search to perform. Defaults to "compound".
                                       - "compound": Search for chemical structures and properties
                                       - "assay": Search for biological assays and experimental protocols  
                                       - "bioactivity": Search for activity measurements and screening results
            
        Returns:
            dict: Search results with structure varying by search_type:
            
            For search_type="compound":
                - results (list): Compound entries with CID, names, SMILES, molecular formula/weight
                - count (int): Number of matching compounds found
                
            For search_type="assay": 
                - results (list): Assay entries with AID, target, type, organism, compound counts
                - count (int): Number of matching assays found
                
            For search_type="bioactivity":
                - results (list): Activity entries with CID, AID, IC50/EC50 values, activity outcomes
                - summary (dict): Statistics on active compounds, targets, confidence scores
                - count (int): Number of activity measurements found
                
            Common fields for all types:
                - query (str): Original search query
                - search_type (str): Type of search performed
                - error (str): Error message if search_type is invalid
                
        Example Usage:
            pubchem_lookup("aspirin", "compound") -> Returns aspirin's structure and properties
            pubchem_lookup("EGFR", "assay") -> Returns assays testing EGFR activity  
            pubchem_lookup("kinase inhibitor", "bioactivity") -> Returns IC50 data for kinase inhibitors
        """
        valid_types = ["compound", "assay", "bioactivity"]
        if search_type not in valid_types:
            return {
                "error": f"Invalid search_type '{search_type}'. Must be one of: {valid_types}",
                "query": query,
                "search_type": search_type
            }
        
        key = f"{query}|{search_type}"
        hash_value = int(hashlib.md5(key.encode()).hexdigest()[:8], 16)
        num_results = 1 + (hash_value % 5)  # Generate 1-5 mock results
        
        results = []
        
        if search_type == "compound":
            # Mock compound search results
            for i in range(num_results):
                cid = 1000 + ((hash_value + i * 37) % 90000)
                compound_names = [
                    f"Compound_{cid}",
                    f"MC-{cid}",
                    f"Test-Compound-{cid % 1000}"
                ]
                smiles = f"C{('C' * ((hash_value + i) % 6))}O"  # Simple alkyl chains with OH
                mw = 200 + ((hash_value + i * 23) % 300)  # MW 200-500
                
                results.append({
                    "cid": cid,
                    "names": compound_names,
                    "smiles": smiles,
                    "molecular_formula": f"C{((hash_value + i) % 6) + 1}H{((hash_value + i) % 6) * 2 + 2}O",
                    "molecular_weight": round(mw, 2),
                    "iupac_name": f"MJ-{((hash_value + i) % 6) + 1}-ol"
                })
                
            return {
                "query": query,
                "search_type": search_type,
                "count": len(results),
                "results": results
            }
        
        elif search_type == "assay":
            # Mock assay search results
            targets = ["EGFR", "VEGFR2", "CDK2", "p53", "BRAF", "ALK", "HER2", "PI3K"]
            assay_types = ["binding", "enzymatic", "cell-based", "functional"]
            
            for i in range(num_results):
                aid = 1000000 + ((hash_value + i * 47) % 900000)  # Assay IDs
                target = targets[(hash_value + i) % len(targets)]
                assay_type = assay_types[(hash_value + i) % len(assay_types)]
                
                results.append({
                    "aid": aid,
                    "title": f"{target} {assay_type} assay",
                    "description": f"{assay_type} assay measuring activity against {target}",
                    "target": target,
                    "assay_type": assay_type,
                    "organism": "Homo sapiens" if (hash_value + i) % 2 == 0 else "Rattus norvegicus",
                    "active_compounds": 50 + ((hash_value + i * 31) % 200),  # 50-250 active compounds
                    "total_compounds": 500 + ((hash_value + i * 41) % 1500)   # 500-2000 total tested
                })
                
            return {
                "query": query,
                "search_type": search_type,
                "count": len(results),
                "results": results
            }
        
        elif search_type == "bioactivity":
            # Mock bioactivity search results
            activity_types = ["IC50", "EC50", "Ki", "Kd", "ED50"]
            units = ["nM", "μM", "pM"]
            
            for i in range(num_results):
                cid = 1000 + ((hash_value + i * 37) % 90000)
                aid = 1000000 + ((hash_value + i * 47) % 900000)
                activity_type = activity_types[(hash_value + i) % len(activity_types)]
                unit = units[(hash_value + i) % len(units)]
                
                # Generate realistic activity values based on unit
                if unit == "nM":
                    value = 1 + ((hash_value + i * 13) % 999)  # 1-1000 nM
                elif unit == "μM":
                    value = round(0.1 + ((hash_value + i * 17) % 99) / 10, 1)  # 0.1-10 μM  
                else:  # pM
                    value = 10 + ((hash_value + i * 19) % 990)  # 10-1000 pM
                
                results.append({
                    "cid": cid,
                    "aid": aid,
                    "compound_name": f"Compound_{cid}",
                    "target": ["EGFR", "VEGFR2", "CDK2", "p53"][(hash_value + i) % 4],
                    "activity_type": activity_type,
                    "activity_value": value,
                    "activity_unit": unit,
                    "activity_outcome": "Active" if value < 1000 else "Inactive",
                    "confidence_score": round(0.6 + ((hash_value + i * 7) % 40) / 100, 2)  # 0.6-1.0
                })
            
            # Calculate summary statistics
            active_count = sum(1 for r in results if r["activity_outcome"] == "Active")
            avg_confidence = round(sum(r["confidence_score"] for r in results) / len(results), 2)
            
            return {
                "query": query,
                "search_type": search_type,
                "count": len(results),
                "results": results,
                "summary": {
                    "active_compounds": active_count,
                    "inactive_compounds": len(results) - active_count,
                    "average_confidence": avg_confidence,
                    "unique_targets": len(set(r["target"] for r in results))
                }
            }
