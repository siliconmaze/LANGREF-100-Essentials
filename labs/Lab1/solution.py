#!/usr/bin/env python3
"""
Lab 1 Solution: Environment Setup Verification
==============================================

Run this to verify your LangGraph environment is correctly set up.
"""

import sys
from typing import TypedDict
from langgraph.graph import StateGraph, END

def main():
    print("=" * 50)
    print("Lab 1: Environment Verification")
    print("=" * 50)
    
    # Test 1: Imports
    print("\n[1] Testing imports...")
    try:
        import langchain
        print(f"    LangChain: {langchain.__version__}")
    except ImportError as e:
        print(f"    ✗ LangChain import failed: {e}")
        return False
    
    try:
        import langgraph
        print(f"    LangGraph: {langgraph.__version__}")
    except ImportError as e:
        print(f"    ✗ LangGraph import failed: {e}")
        return False
    
    # Test 2: Basic graph
    print("\n[2] Testing StateGraph...")
    
    class TestState(TypedDict):
        value: int
        name: str
    
    try:
        graph = StateGraph(TestState)
        
        def node_a(state: TestState) -> TestState:
            return {"value": state["value"] + 1, "name": "node_a"}
        
        graph.add_node("node_a", node_a)
        graph.set_entry_point("node_a")
        graph.add_edge("node_a", END)
        
        compiled = graph.compile()
        result = compiled.invoke({"value": 10, "name": "test"})
        
        print(f"    Input: {{'value': 10, 'name': 'test'}}")
        print(f"    Output: {result}")
        
        if result["value"] == 11 and result["name"] == "node_a":
            print("    ✓ State correctly updated")
        else:
            print("    ✗ Unexpected output")
            return False
            
    except Exception as e:
        print(f"    ✗ Graph test failed: {e}")
        return False
    
    # Test 3: Environment
    print("\n[3] Environment check...")
    from dotenv import load_dotenv
    import os
    
    load_dotenv()
    
    keys = ["DEEPSEEK_API_KEY", "MINIMAX_API_KEY", "OPENAI_API_KEY"]
    for key in keys:
        value = os.getenv(key)
        if value:
            print(f"    ✓ {key}: set")
        else:
            print(f"    ○ {key}: not set (optional)")
    
    print("\n" + "=" * 50)
    print("✓ Lab 1 Complete!")
    print("=" * 50)
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
