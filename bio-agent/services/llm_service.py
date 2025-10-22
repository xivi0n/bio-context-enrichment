"""
Simple LLM service for query routing and understanding.
"""

import json
import logging
import os
from typing import Dict, Any, List, Optional
from dotenv import load_dotenv
import openai
from prompts.router import build_router_system_prompt
from prompts.reasoner import (
    build_reasoner_system_prompt,
    build_reasoner_prompt_with_context,
)

load_dotenv()

logger = logging.getLogger(__name__)

# Global OpenAI client instance
openai_client = None


def initialize_client():
    """
    Initialize the global OpenAI client using environment configuration.
    """
    global openai_client

    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        logger.error("OPENAI_API_KEY not found in environment variables")
        return

    openai_client = openai.OpenAI(api_key=api_key)
    logger.info("OpenAI client initialized successfully")


def llm_router(
    input_prompt: str,
    available_tools: List[Dict[str, Any]],
    model: str = None,
) -> Dict[str, Any]:
    """
    Route and understand user queries using LLM.

    Args:
        input_prompt: The user's input query
        available_tools: List of available tools with name, description, and schema
        model: OpenAI model to use (default: uses ROUTER_MODEL env var or gpt-4o-mini)

    Returns:
        Parsed JSON response with action, tools needed, entities, etc.
    """
    if openai_client is None:
        logger.error("OpenAI client not initialized")
        return {"error": "OpenAI client not initialized"}

    # Use environment variable or fallback to default
    if model is None:
        model = os.environ.get("ROUTER_MODEL", "gpt-4.1-mini")

    try:
        supported_actions = get_supported_actions()
        logger.info(
            f"Available tools for routing: {[tool['name'] for tool in available_tools]}"
        )
        system_prompt = build_router_system_prompt(available_tools, supported_actions)

        response = openai_client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": input_prompt},
            ],
        )

        # Extract the content from the response
        content = response.choices[0].message.content.strip()

        # Parse JSON response
        try:
            parsed_response = json.loads(content)
            logger.info(
                f"Successfully routed query with action: {parsed_response.get('action', 'unknown')}"
            )
            return parsed_response

        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON response: {content}")
            return {
                "error": "Invalid JSON response from LLM",
                "raw_response": content,
                "parse_error": str(e),
            }

    except Exception as e:
        logger.error(f"Failed to call OpenAI API: {str(e)}")
        return {"error": str(e)}


def get_supported_actions() -> Dict[str, str]:
    """
    Get dictionary of supported actions with their descriptions.

    Returns:
        Dictionary mapping action names to their descriptions
    """
    return {
        "rank": "Rank and order biological entities, proteins, genes, or research papers based on relevance, importance, or specific criteria",
        "select": "Select and filter specific biological entities, datasets, or information based on given parameters or conditions",
        "explain": "Provide detailed explanations about biological concepts, processes, research findings, or entity relationships",
    }


def llm_reasoner(
    prompt: str,
    decision: str,
    tool_results: List[Dict[str, Any]],
    model: str = None,
) -> Dict[str, Any]:
    """
    Analyze tool results and make informed decisions based on the context.

    Args:
        prompt: The original user query/prompt
        decision: The decision context or specific question to be answered
        tool_results: List of results from various tools
        model: OpenAI model to use (default: uses REASONER_MODEL env var or gpt-4o)

    Returns:
        JSON response with result and rationale
    """
    if openai_client is None:
        logger.error("OpenAI client not initialized")
        return {"error": "OpenAI client not initialized"}

    # Use environment variable or fallback to default
    if model is None:
        model = os.environ.get("REASONER_MODEL", "gpt-4.1")

    try:
        logger.info(f"Running reasoning analysis with {len(tool_results)} tool results")

        system_prompt = build_reasoner_system_prompt()
        user_prompt = build_reasoner_prompt_with_context(prompt, decision, tool_results)

        response = openai_client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
        )

        # Extract the content from the response
        content = response.choices[0].message.content.strip()

        # Parse JSON response
        try:
            parsed_response = json.loads(content)

            # Validate the required fields
            if "result" not in parsed_response or "rationale" not in parsed_response:
                logger.error(f"Invalid response format: missing required fields")
                return {
                    "error": "Invalid response format: missing 'result' or 'rationale' fields",
                    "raw_response": content,
                }

            logger.info(f"Successfully completed reasoning analysis")
            return parsed_response

        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON response: {content}")
            return {
                "error": "Invalid JSON response from LLM",
                "raw_response": content,
                "parse_error": str(e),
            }

    except Exception as e:
        logger.error(f"Failed to call OpenAI API: {str(e)}")
        return {"error": str(e)}
