"""
Test configuration and fixtures for bio-agent tests.
"""

import pytest
import os
from unittest.mock import Mock, patch
from app import app as flask_app


@pytest.fixture
def app():
    """Create and configure a test Flask app."""
    flask_app.config.update({"TESTING": True, "WTF_CSRF_ENABLED": False})
    return flask_app


@pytest.fixture
def client(app):
    """Create a test client for the Flask app."""
    return app.test_client()


@pytest.fixture
def mock_openai_client():
    """Mock OpenAI client for testing."""
    with patch("services.llm_service.openai_client") as mock_client:
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message = Mock()
        mock_response.choices[0].message.content = (
            '{"needs_tools": false, "reasoning": "test"}'
        )
        mock_client.chat.completions.create.return_value = mock_response
        yield mock_client


@pytest.fixture
def mock_mcp_client():
    """Mock MCP client for testing."""
    with (
        patch("services.tools_service.get_tools_list") as mock_tools,
        patch("services.tools_service.call_tool") as mock_call,
    ):
        mock_tools.return_value = [{"name": "test_tool", "description": "Test tool"}]
        mock_call.return_value = {"result": "success"}
        yield mock_tools, mock_call


@pytest.fixture
def sample_prompt():
    """Sample prompt for testing."""
    return {"prompt": "What is the function of the BRCA1 gene?"}


@pytest.fixture
def mock_env_vars():
    """Mock environment variables for testing."""
    with patch.dict(os.environ, {"OPENAI_API_KEY": "test_key", "PORT": "5050"}):
        yield
