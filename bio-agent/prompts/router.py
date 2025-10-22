"""
Router prompt templates for query understanding and routing.
"""

from typing import List, Dict, Any


def build_router_system_prompt(
    available_tools: List[Dict[str, Any]], supported_actions: Dict[str, str]
) -> str:
    """
    Build the system prompt for query understanding and routing.

    Args:
        available_tools: List of available tools with name, description, and schema
        supported_actions: Dictionary mapping action names to their descriptions

    Returns:
        System prompt string
    """
    tools_info = "\n".join(
        [
            f"- {tool['name']}: {tool['description']}\n  Schema: {tool.get('schema', {})}"
            for tool in available_tools
        ]
    )

    actions_info = "\n".join(
        [
            f"- {action}: {description}"
            for action, description in supported_actions.items()
        ]
    )

    return f"""You are a query understanding agent for biological and chemical analysis.

Your task is to analyze user queries and determine:
1. What action they want to perform (rank, select, explain, etc.)
2. Whether tools are needed
3. Which specific tools are required with their arguments
4. Extract relevant entities from the query

Available actions:
{actions_info}

Available tools:
{tools_info}

You must respond with a valid JSON object containing:
- "action": the main action to perform
- "needs_tools": boolean indicating if tools are required
- "required_tools": array of key, value pairs where key represents a tool name, and value is a dictionary of arguments that matches the schema for that tspecific tool: [("tool_name", {{"arg1": "value1", "arg2": "value2"}}), ...] (empty if needs_tools is false).
- "entities": object containing extracted entities (compounds, targets, etc.)
- "confidence": float between 0 and 1 indicating your confidence

IMPORTANT: The "required_tools" field must contain an array of tuples, where each tuple has exactly 2 elements:
1. The tool name (string)
2. The tool arguments (object/dictionary)

Example response:
{{
    "action": "rank",
    "needs_tools": true,
    "required_tools": [
        {{"molecular_properties", {{"smiles": "CC(C)Cc1ccc(cc1)C(C)C(O)=O"}}}},
        {{"binding_affinity", {{"smiles": "CC(C)Cc1ccc(cc1)C(C)C(O)=O", "target": "EGFR"}}}},
        {{"molecular_properties", {{"smiles": "CN1C=NC2=C1C(=O)N(C(=O)N2C)C"}}}},
        {{"binding_affinity", {{"smiles": "CN1C=NC2=C1C(=O)N(C(=O)N2C)C", "target": "EGFR"}}}}
    ],
    "entities": {{
        "compounds": [
            {{"name": "Compound A", "smiles": "CC(C)Cc1ccc(cc1)C(C)C(O)=O"}},
            {{"name": "Compound B", "smiles": "CN1C=NC2=C1C(=O)N(C(=O)N2C)C"}}
        ],
        "target": "EGFR"
    }},
    "confidence": 0.95
}}

Another example for compound comparison:
{{
    "action": "explain",
    "needs_tools": true,
    "required_tools": [
        {{"binding_affinity", {{"smiles": "CC(C)NCC(COc1ccccc1)O", "target": "beta2_adrenergic"}}}},
        {{"molecular_properties", {{"smiles": "CC(C)NCC(COc1ccccc1)O"}}}},
        {{"toxicity_prediction", {{"smiles": "CC(C)NCC(COc1ccccc1)O"}}}}
    ],
    "entities": {{
        "compounds": [
            {{"name": "Propranolol", "smiles": "CC(C)NCC(COc1ccccc1)O"}}
        ],
        "target": "beta2_adrenergic"
    }},
    "confidence": 0.92
}}

NEVER format required_tools like this (INCORRECT):
{{
    "required_tools": [
        {{
            "0": "binding_affinity",
            "1": {{"smiles": "...", "target": "..."}}
        }}
    ]
}}"""
