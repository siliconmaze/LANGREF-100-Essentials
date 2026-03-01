#!/usr/bin/env python3
"""
Lab 4 Solution: Persistence & Checkpointing
============================================
"""

from typing import TypedDict
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
import uuid

class CounterState(TypedDict):
    count: int
    history: list

def increment(state: CounterState) -> CounterState:
    new_count = state["count"] + 1
    return {
        "count": new_count,
        "history": state["history"] + [new_count]
    }

def should_continue(state: CounterState) -> str:
    if state["count"] < 5:
        return "increment"
    return "end"

def main():
    print("=" * 50)
    print("Lab 4: Persistence & Checkpointing")
    print("=" * 50)
    
    # Create checkpointer
    checkpointer = MemorySaver()
    
    # Build graph
    graph = StateGraph(CounterState)
    graph.add_node("increment", increment)
    graph.set_entry_point("increment")
    graph.add_conditional_edges(
        "increment",
        should_continue,
        {
            "increment": "increment",
            "end": END
        }
    )
    
    app = graph.compile(checkpointer=checkpointer)
    
    # Use unique thread ID
    thread_id = f"counter-{uuid.uuid4().hex[:8]}"
    config = {"configurable": {"thread_id": thread_id}}
    
    print(f"\nThread ID: {thread_id}")
    print("Running counter from 0...")
    
    # Run
    result = app.invoke({"count": 0, "history": []}, config)
    
    print(f"Final result: {result}")
    
    # Verify state was saved
    saved_state = app.get_state(config)
    print(f"Saved state: {saved_state.values}")
    
    # Resume (would continue from 5 in real scenario)
    print("\n✓ Lab 4 Complete!")
    return True

if __name__ == "__main__":
    main()
