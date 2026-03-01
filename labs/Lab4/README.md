# Lab 4: Persistence & Checkpointing

## Objectives

- Save and resume graph state
- Use checkpointer
- Implement memory
- Handle interruptions

## Duration

45 minutes

---

## Why Persistence?

Without persistence:
- State lost on restart
- No conversation memory
- Can't resume after error

With persistence:
- State saved to disk
- Resume anytime
- Maintain context

---

## Checkpoint Basics

```python
from langgraph.checkpoint.memory import MemorySaver

# Create checkpointer
checkpointer = MemorySaver()

# Compile with checkpointer
graph = StateGraph(AgentState)
# ... add nodes ...
app = graph.compile(checkpointer=checkpoint)
```

---

## Saving State

```python
# Run with thread_id
config = {"configurable": {"thread_id": "user-123"}}
result = app.invoke({"messages": ["Hi"]}, config)
```

State is now saved!

---

## Resuming State

```python
# Same thread_id = resumes from saved state
config = {"configurable": {"thread_id": "user-123"}}
result = app.invoke({"messages": ["Hello again"]}, config)
```

---

## Using SQLite Checkpointer

```python
from langgraph.checkpoint.sqlite import SqliteSaver

# File-based persistence
checkpointer = SqliteSaver.from_conn_string("langgraph.db")

app = graph.compile(checkpointer=checkpointer)
```

---

## Example: Conversation Memory

```python
from typing import TypedDict
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver

class ChatState(TypedDict):
    messages: list

def chat_node(state: ChatState) -> ChatState:
    user_msg = state["messages"][-1]
    response = f"Echo: {user_msg}"
    return {"messages": state["messages"] + [response]}

# Setup
checkpointer = MemorySaver()
graph = StateGraph(ChatState)
graph.add_node("chat", chat_node)
graph.set_entry_point("chat")
graph.add_edge("chat", END)

app = graph.compile(checkpointer=checkpointer)

# First message
config = {"configurable": {"thread_id": "session-1"}}
app.invoke({"messages": ["Hello"]}, config)

# Resume with second message
app.invoke({"messages": ["How are you?"]}, config)

# Check saved state
state = app.get_state(config)
print(state.values["messages"])
# ['Hello', 'Echo: Hello', 'How are you?', 'Echo: How are you?']
```

---

## Exercises

### Exercise 4.1: Simple Persistence
Create a counter that:
- Saves state after each increment
- Can be resumed from saved count

### Exercise 4.2: Multi-User Chat
Implement:
- Multiple users (thread_ids)
- Each user has own conversation
- Checkpoint persists across restarts

### Exercise 4.3: Long-Running Task
Build a task that:
- Saves progress at each step
- Can be interrupted and resumed

---

## Key Concepts

| Concept | Description |
|---------|-------------|
| **Checkpointer** | Saves/loads graph state |
| **MemorySaver** | In-memory persistence |
| **SqliteSaver** | File-based persistence |
| **thread_id** | Unique identifier for state |

---

## Summary

✓ Added checkpointer to graph  
✓ Saved and resumed state  
✓ Implemented conversation memory  
✓ Used SQLite persistence  

---

## Next Lab

[Lab 5: Production Patterns](../Lab5/README.md)
