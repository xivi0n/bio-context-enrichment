"""
Test cases for Flask app endpoints.
"""

import json
from unittest.mock import patch


class TestHealthEndpoint:
    """Test cases for the /health endpoint."""

    def test_health_check_returns_success(self, client):
        """Test that health check returns healthy status."""
        response = client.get("/health")
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["status"] == "healthy"


class TestToolsEndpoint:
    """Test cases for the /tools endpoint."""

    def test_list_tools_success(self, client):
        """Test successful tools listing."""

        response = client.get("/tools")
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["status"] == "success"
        assert "tools" in data
        assert "count" in data
        assert data["count"] == len(data["tools"])

    def test_list_tools_failure(self, client):
        """Test tools listing when MCP client fails."""
        with patch("app.get_tools_list", side_effect=Exception("MCP error")):
            response = client.get("/tools")
            assert response.status_code == 500
            data = json.loads(response.data)
            assert "error" in data
            assert data["error"] == "Failed to retrieve tools"


class TestPromptEndpoint:
    """Test cases for the /prompt endpoint."""

    def test_prompt_missing_data(self, client):
        """Test prompt endpoint with missing request data."""
        response = client.post(
            "/prompt", data=json.dumps({}), content_type="application/json"
        )
        assert response.status_code == 400
        data = json.loads(response.data)
        assert "error" in data
        assert "Missing prompt" in data["error"]

    def test_prompt_missing_prompt_key(self, client):
        """Test prompt endpoint with missing prompt key."""
        response = client.post(
            "/prompt",
            data=json.dumps({"message": "test"}),
            content_type="application/json",
        )
        assert response.status_code == 400
        data = json.loads(response.data)
        assert "error" in data
        assert "Missing prompt" in data["error"]

    def test_prompt_success_no_tools(self, client, sample_prompt):
        """Test successful prompt processing without tool usage."""
        with (
            patch("app.llm_router") as mock_router,
            patch("app.llm_reasoner") as mock_reasoner,
        ):

            mock_router.return_value = {
                "needs_tools": False,
                "reasoning": "No tools needed",
            }
            mock_reasoner.return_value = "This is about the BRCA1 gene function."

            response = client.post(
                "/prompt",
                data=json.dumps(sample_prompt),
                content_type="application/json",
            )

            assert response.status_code == 200
            data = json.loads(response.data)
            assert data["status"] == "success"
            assert data["prompt"] == sample_prompt["prompt"]
            assert "decision" in data
            assert "tool_results" in data
            assert "response" in data

    def test_prompt_success_with_tools(self, client, sample_prompt):
        """Test successful prompt processing with tool usage."""
        with (
            patch("app.llm_router") as mock_router,
            patch("app.llm_reasoner") as mock_reasoner,
        ):

            mock_router.return_value = {
                "needs_tools": True,
                "required_tools": [{"search_gene": {"gene": "BRCA1"}}],
            }
            mock_reasoner.return_value = "BRCA1 is a tumor suppressor gene."

            response = client.post(
                "/prompt",
                data=json.dumps(sample_prompt),
                content_type="application/json",
            )

            assert response.status_code == 200
            data = json.loads(response.data)
            assert data["status"] == "success"
            assert len(data["tool_results"]) > 0

    def test_prompt_internal_error(self, client, sample_prompt):
        """Test prompt endpoint with internal server error."""
        with patch("app.get_tools_list", side_effect=Exception("Internal error")):
            response = client.post(
                "/prompt",
                data=json.dumps(sample_prompt),
                content_type="application/json",
            )

            assert response.status_code == 500
            data = json.loads(response.data)
            assert "error" in data
            assert data["error"] == "Internal server error"
