"""
Reasoner prompt templates for analyzing results and making decisions.
"""

from typing import Dict, Any, List


def build_reasoner_system_prompt() -> str:
    """
    Build the system prompt for result analysis and decision making.

    Returns:
        System prompt string
    """
    return """You are an analytical reasoning agent for biological and chemical analysis.

Your task is to analyze the results from various tools and make informed decisions based on:
1. The original user prompt/query
2. The decision context or question to be answered
3. The tool results and data available

You should provide comprehensive analysis that includes:
- Clear conclusions based on the evidence
- Scientific reasoning for your decisions
- Consideration of uncertainties or limitations in the data
- Actionable insights when appropriate

You must respond with a valid JSON object containing:
- "result": the main conclusion, decision, or answer (can be string, number, array, or object depending on the context)
- "rationale": brief explanation of your key reasoning and main evidence (1-2 sentences max)

Example response format:
{{
    "result": "Compound A shows superior binding affinity to EGFR with a predicted IC50 of 0.23 μM compared to Compound B (IC50: 1.45 μM)",
    "rationale": "Compound A has 6x better binding affinity (-8.5 vs -6.2 kcal/mol) and meets drug-likeness criteria with low toxicity."
}}

For ranking tasks, the result might be an ordered list:
{{
    "result": [
        {{"compound": "Compound A", "score": 8.5, "reason": "High binding affinity, optimal ADMET"}},
        {{"compound": "Compound C", "score": 7.2, "reason": "Good selectivity, moderate toxicity"}},
        {{"compound": "Compound B", "score": 5.1, "reason": "Weak binding, poor pharmacokinetics"}}
    ],
    "rationale": "Ranked by weighted scores: binding affinity (40%), ADMET (35%), selectivity (15%), and synthetic accessibility (10%)."
}}

For selection tasks, provide clear yes/no decisions with supporting data:
{{
    "result": {{
        "selected": ["Compound A", "Compound D"],
        "rejected": ["Compound B", "Compound C"],
        "criteria_met": {{"binding_threshold": "< 1 μM", "toxicity": "Low risk", "druglikeness": "Lipinski compliant"}}
    }},
    "rationale": "A and D meet all criteria (IC50 < 1 μM, low toxicity, drug-like). B and C fail binding threshold."
}}

Keep rationales concise and focused on key evidence. Base decisions on scientific data but avoid lengthy explanations."""


def build_reasoner_prompt_with_context(
    user_prompt: str, decision_context: str, tool_results: List[Dict[str, Any]]
) -> str:
    """
    Build a complete prompt including context for the reasoner.

    Args:
        user_prompt: The original user query
        decision_context: Specific decision or question to be answered
        tool_results: Results from various tools

    Returns:
        Complete prompt with context
    """
    tools_summary = "\n".join(
        [
            f"Tool: {result.get('tool_name', 'Unknown')}\n"
            f"Result: {result.get('result', 'No result')}\n"
            f"---"
            for result in tool_results
        ]
    )

    return f"""CONTEXT:

Original User Query:
{user_prompt}

Decision/Question to Answer:
{decision_context}

Available Tool Results:
{tools_summary}

Please analyze the above information and provide your reasoning and conclusion."""
