from flask import Flask, request, jsonify
import logging
import asyncio
import os
from dotenv import load_dotenv
from services.tools_service import (
    get_tools_list,
    call_tool,
    initialize_client as initialize_mcp_client,
)
from services.llm_service import (
    initialize_client as initialize_llm_client,
    llm_router,
    llm_reasoner,
)

load_dotenv()

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

app = Flask(__name__)


def initialize_client():
    """
    Initialize the MCP client and LLM client
    """
    logger.info("Initializing MCP client...")
    initialize_mcp_client()
    logger.info("MCP client initialization completed")

    logger.info("Initializing LLM client...")
    initialize_llm_client()
    logger.info("LLM client initialization completed")


@app.route("/prompt", methods=["POST"])
def handle_prompt():
    """
    Endpoint to receive and log prompts
    """
    try:
        data = request.get_json()

        if not data or "prompt" not in data:
            return jsonify({"error": "Missing prompt in request body"}), 400

        prompt = data["prompt"]
        logger.info(f"Received prompt: {prompt}")

        tools = asyncio.run(get_tools_list())
        decision = llm_router(prompt, tools)
        logger.info(f"LLM Router decision: {decision}")

        tool_results = []
        if "needs_tools" in decision and decision["needs_tools"]:
            for required_tool in decision.get("required_tools", []):
                logger.info(f"Calling tool: {required_tool}")
                for tool_name, tool_args in required_tool.items():
                    tool_result = asyncio.run(call_tool(tool_name, tool_args))
                    tool_results.append(
                        {
                            "tool_name": tool_name,
                            "args": tool_args,
                            "result": tool_result,
                        }
                    )
                    logger.info(
                        f"Tool {tool_name} called with args {tool_args}, result: {tool_result}"
                    )

        response = llm_reasoner(prompt, decision, tool_results)

        logger.info("Prompt processing completed successfully")

        return (
            jsonify(
                {
                    "status": "success",
                    "prompt": prompt,
                    "decision": decision,
                    "tool_results": tool_results,
                    "response": response,
                }
            ),
            200,
        )

    except Exception as e:
        logger.error(f"Error processing prompt: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500


@app.route("/health", methods=["GET"])
def health_check():
    """
    Simple health check endpoint
    """
    return jsonify({"status": "healthy"}), 200


@app.route("/tools", methods=["GET"])
def list_tools():
    """
    Endpoint to list all available tools from MCP client
    """
    try:
        tools = asyncio.run(get_tools_list())
        return jsonify({"status": "success", "tools": tools, "count": len(tools)}), 200

    except Exception as e:
        logger.error(f"Error listing tools: {str(e)}")
        return jsonify({"error": "Failed to retrieve tools"}), 500


if __name__ == "__main__":
    # Get port from environment variable, default to 5050
    port = int(os.environ.get("PORT", "5050"))

    logger.info(f"Starting bio-agent Flask app on port {port}...")

    # Initialize MCP client before starting the server
    initialize_client()

    app.run(port=port, debug=True)
