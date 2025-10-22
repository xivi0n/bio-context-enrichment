"""
Test cases for LLM service functions.
"""

import json
from unittest.mock import Mock, patch
from services.llm_service import (
    initialize_client,
    llm_router,
    llm_reasoner,
)


class TestInitializeClient:
    """Test cases for LLM client initialization."""

    def test_initialize_client_success(self):
        """Test successful client initialization."""
        with patch("services.llm_service.openai.OpenAI") as mock_openai:
            initialize_client()
            mock_openai.assert_called_once_with(api_key="test_key")

    def test_initialize_client_missing_key(self):
        """Test client initialization with missing API key."""
        with patch.dict("os.environ", {}, clear=True):
            with patch("services.llm_service.logger") as mock_logger:
                initialize_client()
                mock_logger.error.assert_called_once()


class TestLLMRouter:
    """Test cases for LLM router function."""

    def test_llm_router_success(self):
        """Test successful LLM routing."""
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message = Mock()
        mock_response.choices[0].message.content = json.dumps(
            {
                "action": "select",
                "reasoning": "This query requires gene information tools",
            }
        )

        with patch("services.llm_service.openai_client") as mock_client:
            mock_client.chat.completions.create.return_value = mock_response

            # Need to provide tools with proper description field
            tools = [
                {"name": "search_gene", "description": "Search for gene information"}
            ]
            result = llm_router("What is BRCA1?", tools)

            assert result["action"] == "select"
            assert "reasoning" in result
            mock_client.chat.completions.create.assert_called_once()

    def test_llm_router_no_tools_needed(self):
        """Test LLM router when no tools are needed."""
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message = Mock()
        mock_response.choices[0].message.content = json.dumps(
            {
                "action": "explain",
                "reasoning": "This is a general question that doesn't require tools",
            }
        )

        with patch("services.llm_service.openai_client") as mock_client:
            mock_client.chat.completions.create.return_value = mock_response

            result = llm_router("Hello", [])

            assert result["action"] == "explain"
            assert "reasoning" in result

    def test_llm_router_invalid_json_response(self):
        """Test LLM router with invalid JSON response."""
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message = Mock()
        mock_response.choices[0].message.content = "Invalid JSON"

        with patch("services.llm_service.openai_client") as mock_client:
            mock_client.chat.completions.create.return_value = mock_response

            result = llm_router("Test query", [])

            # Should return error structure
            assert "error" in result
            assert "Invalid JSON response from LLM" in result["error"]

    def test_llm_router_openai_error(self):
        """Test LLM router when OpenAI API fails."""
        with patch("services.llm_service.openai_client") as mock_client:
            mock_client.chat.completions.create.side_effect = Exception("API Error")

            result = llm_router("Test query", [])

            # Should return error structure
            assert "error" in result
            assert result["error"] == "API Error"


class TestLLMReasoner:
    """Test cases for LLM reasoner function."""

    def test_llm_reasoner_success(self):
        """Test successful LLM reasoning."""
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message = Mock()
        mock_response.choices[0].message.content = json.dumps(
            {
                "result": "BRCA1 is a tumor suppressor gene.",
                "rationale": "Based on scientific knowledge, BRCA1 functions in DNA repair.",
            }
        )

        with patch("services.llm_service.openai_client") as mock_client:
            mock_client.chat.completions.create.return_value = mock_response

            result = llm_reasoner("What is BRCA1?", {"action": "explain"}, [])

            assert result["result"] == "BRCA1 is a tumor suppressor gene."
            assert "rationale" in result
            mock_client.chat.completions.create.assert_called_once()

    def test_llm_reasoner_with_tool_results(self):
        """Test LLM reasoner with tool results."""
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message = Mock()
        mock_response.choices[0].message.content = json.dumps(
            {
                "result": "Based on the search results, BRCA1 is important for DNA repair.",
                "rationale": "The tool provided information about BRCA1's function in DNA repair mechanisms.",
            }
        )

        with patch("services.llm_service.openai_client") as mock_client:
            mock_client.chat.completions.create.return_value = mock_response

            tool_results = [
                {
                    "tool_name": "search_gene",
                    "args": {"gene": "BRCA1"},
                    "result": {"function": "DNA repair"},
                }
            ]

            result = llm_reasoner(
                "What is BRCA1?",
                {
                    "action": "select",
                    "required_tools": [{"search_gene": {"gene": "BRCA1"}}],
                },
                tool_results,
            )

            assert "DNA repair" in result["result"]

    def test_llm_reasoner_openai_error(self):
        """Test LLM reasoner when OpenAI API fails."""
        with patch("services.llm_service.openai_client") as mock_client:
            mock_client.chat.completions.create.side_effect = Exception("API Error")

            result = llm_reasoner("Test query", {"action": "explain"}, [])

            # Should return error structure
            assert isinstance(result, dict)
            assert "error" in result
            assert result["error"] == "API Error"
