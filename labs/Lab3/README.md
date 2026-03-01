# Lab 3: Conditional Edges

## Objectives

- Route based on state
- Use conditional edges
- Create decision logic
- Build branching workflows

## Duration

45 minutes

---

## Conditional Edges

Conditional edges let you **route to different nodes** based on state:

```python
def should_continue(state: AgentState) -> str:
    if state["count"] < 5:
        return "increment"
    return END
```

Then add to graph:

```python
graph.add_conditional_edges(
    "node_name",
    should_continue,
    {
        "increment": "increment_node",
        "decrement": "decrement_node", 
        END: END
    }
)
```

---

## Example: Counter Loop

```python
from typing import TypedDict
from langgraph.graph import StateGraph, END

class LoopState(TypedDict):
    count: int
    history: list

def increment(state: LoopState) -> LoopState:
    return {"count": state["count"] + 1}

def should_continue(state: LoopState) -> str:
    if state["count"] < 5:
        return "increment"
    return "end"

graph = StateGraph(LoopState)
graph.add_node("increment", increment)
graph.set_entry_point("increment")

# Conditional edge
graph.add_conditional_edges(
    "increment",
    should_continue,
    {
        "increment": "increment",
        "end": END
    }
)

app = graph.compile()
result = app.invoke({"count": 0, "history": []})
# Result: {'count': 5, 'history': []}
```

---

## Multiple Conditions

```python
def route_message(state: AgentState) -> str:
    msg = state["messages"][-1].lower()
    
    if "hello" in msg:
        return "greeting"
    elif "help" in msg:
        return "support"
    else:
        return "fallback"

graph.add_conditional_edges(
    "classifier",
    route_message,
    {
        "greeting": "greeting_node",
        "support": "support_node", 
        "fallback": "fallback_node"
    }
)
```

---

## Exercises

### Exercise 3.1: Even/Odd Checker
Create a counter that:
- Loops until count reaches 10
- Tracks if count is even or odd at each step

### Exercise 3.2: Message Router
Build a router that:
- Takes user input
- Routes to: `greeting`, `question`, or `other`
- Each route prints appropriate response

### Exercise 3.3: Grade Classifier
Input: `{"score": 85}`
Output: `{"grade": "A", "feedback": "Excellent!"}`

Rules:
- 90+: A (Excellent)
- 80-89: B (Good)
- 70-79: C (Fair)
- <70: F (Needs improvement)

---

## Key Concepts

| Concept | Description |
|---------|-------------|
| **Conditional Edge** | Routes based on function return |
| **Return value** | Must match keys in mapping dict |
| **END** | Special key for terminating |

---

## Summary

✓ Created conditional routing  
✓ Built decision logic  
✓ Implemented loops  
✓ Handled multiple paths  

---

## Next Lab

[Lab 4: Persistence](../Lab4/README.md)
