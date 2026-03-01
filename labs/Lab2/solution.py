#!/usr/bin/env python3
"""
Lab 2 Solution: State & Nodes
==============================
"""

from typing import TypedDict
from langgraph.graph import StateGraph, END

class AgentState(TypedDict):
    name: str
    greeting: str
    keywords: list
    formatted: str

def extract_keywords(state: AgentState) -> AgentState:
    """Extract keywords from text."""
    text = state.get("name", "")
    # Simple keyword extraction
    words = text.lower().split()
    return {"keywords": words}

def transform_keywords(state: AgentState) -> AgentState:
    """Transform keywords to uppercase."""
    keywords = state.get("keywords", [])
    return {"keywords": [k.upper() for k in keywords]}

def format_output(state: AgentState) -> AgentState:
    """Format final output."""
    keywords = state.get("keywords", [])
    name = state.get("name", "User")
    formatted = f"Hello {name}! Keywords: {', '.join(keywords)}"
    return {"formatted": formatted, "greeting": f"Hello {name}!"}

def main():
    print("=" * 50)
    print("Lab 2: State & Nodes")
    print("=" * 50)
    
    # Build the graph
    graph = StateGraph(AgentState)
    
    graph.add_node("extract", extract_keywords)
    graph.add_node("transform", transform_keywords)
    graph.add_node("format", format_output)
    
    graph.set_entry_point("extract")
    graph.add_edge("extract", "transform")
    graph.add_edge("transform", "format")
    graph.add_edge("format", END)
    
    # Compile and run
    app = graph.compile()
    
    # Test input
    result = app.invoke({"name": "John Doe"})
    
    print(f"\nInput: {{'name': 'John Doe'}}")
    print(f"Output: {result}")
    
    print("\n✓ Lab 2 Complete!")
    return True

if __name__ == "__main__":
    main()
