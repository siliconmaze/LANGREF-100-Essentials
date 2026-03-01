# Lab 2: State & Nodes

## Objectives

- Understand LangGraph state management
- Create custom nodes
- Pass data between nodes
- Use multiple node types

## Duration

45 minutes

---

## Understanding State

State is a **TypedDict** that flows through your graph:

```python
from typing import TypedDict

class AgentState(TypedDict):
    messages: list[str]
    context: dict
    step: int
```

---

## Creating Nodes

Nodes are Python functions that:
1. Receive state as input
2. Process/transform data
3. Return updated state

```python
def my_node(state: AgentState) -> AgentState:
    # Process state
    new_value = do_something(state["value"])
    
    # Return updates (not full state)
    return {"value": new_value}
```

---

## Example: Simple Counter

```python
from typing import TypedDict
from langgraph.graph import StateGraph, END

# 1. Define state
class CounterState(TypedDict):
    count: int

# 2. Create nodes
def increment(state: CounterState) -> CounterState:
    return {"count": state["count"] + 1}

def decrement(state: CounterState) -> CounterState:
    return {"count": state["count"] - 1}

# 3. Build graph
graph = StateGraph(CounterState)

graph.add_node("increment", increment)
graph.add_node("decrement", decrement)

graph.set_entry_point("increment")
graph.add_edge("increment", "decrement")
graph.add_edge("decrement", END)

# 4. Run
app = graph.compile()
result = app.invoke({"count": 0})
print(result)  # {'count': -1}
```

---

## Multiple State Updates

Nodes can update multiple fields:

```python
def process_data(state: AgentState) -> AgentState:
    messages = state["messages"]
    last_msg = messages[-1]
    
    return {
        "context": {"last_message": last_msg},
        "step": state["step"] + 1
    }
```

---

## Node with External Calls

```python
def fetch_data(state: AgentState) -> AgentState:
    # Call external API
    data = api.get(state["query"])
    
    return {"results": data}
```

---

## Exercises

### Exercise 2.1: Name Processor
Create nodes that:
1. Take input: `{"name": "John"}`
2. Transform to: `{"name": "John", "greeting": "Hello John!"}`

### Exercise 2.2: Multi-Step Pipeline
Build a 3-node pipeline:
1. `extract` - Extract keywords from text
2. `transform` - Convert keywords to uppercase
3. `format` - Create final output

### Exercise 2.3: State Counter
Create a graph that counts to 5 using a loop (see conditional edges in Lab 3).

---

## Key Concepts

| Concept | Description |
|---------|-------------|
| **State** | TypedDict defining your data shape |
| **Node** | Function that processes state |
| **add_node()** | Register a node in the graph |
| **Return** | Partial state updates (not full) |

---

## Summary

✓ Defined custom state types  
✓ Created processing nodes  
✓ Connected nodes with edges  
✓ Ran the graph  

---

## Next Lab

[Lab 3: Conditional Edges](../Lab3/README.md)
