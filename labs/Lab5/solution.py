#!/usr/bin/env python3
"""
Lab 5 Solution: Production Patterns
=================================
"""

import logging
import os
import uuid
from typing import TypedDict
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from dotenv import load_dotenv

load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("langgraph")

class Config:
    """Application configuration."""
    MAX_RETRIES = int(os.getenv("MAX_RETRIES", "3"))
    TIMEOUT = int(os.getenv("TIMEOUT", "30"))
    DEBUG = os.getenv("DEBUG", "false").lower() == "true"

class AgentState(TypedDict):
    data: str
    status: str
    error: str | None

def safe_node(state: AgentState) -> AgentState:
    """Node with error handling."""
    logger.info("Processing safe_node")
    try:
        # Simulate processing
        result = f"Processed: {state['data']}"
        logger.info("Node completed successfully")
        return {"status": "success", "data": result, "error": None}
    except Exception as e:
        logger.error(f"Node failed: {e}")
        return {"status": "failed", "error": str(e)}

def health_check_node(state: AgentState) -> AgentState:
    """Health check node."""
    return {"status": "healthy", "data": "OK"}

def main():
    print("=" * 50)
    print("Lab 5: Production Patterns")
    print("=" * 50)
    
    print(f"\nConfig: MAX_RETRIES={Config.MAX_RETRIES}, TIMEOUT={Config.TIMEOUT}")
    print(f"Debug mode: {Config.DEBUG}")
    
    # Build graph with error handling
    checkpointer = MemorySaver()
    graph = StateGraph(AgentState)
    
    graph.add_node("safe_node", safe_node)
    graph.add_node("health_check", health_check_node)
    
    graph.set_entry_point("safe_node")
    graph.add_edge("safe_node", "health_check")
    graph.add_edge("health_check", END)
    
    app = graph.compile(checkpointer=checkpointer)
    
    # Test with config
    config = {"configurable": {"thread_id": f"test-{uuid.uuid4().hex[:8]}"}}
    
    print("\n[1] Testing normal flow...")
    result = app.invoke({"data": "test", "status": "", "error": ""}, config)
    print(f"Result: {result}")
    
    print("\n✓ Lab 5 Complete!")
    print("\nProduction readiness checklist:")
    print("  ✓ Error handling implemented")
    print("  ✓ Logging configured")
    print("  ✓ Environment config")
    print("  ✓ Health check patterns")
    
    return True

if __name__ == "__main__":
    main()
