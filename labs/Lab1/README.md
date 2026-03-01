# Lab 1: Environment Setup

## Objectives

- Set up Python virtual environment
- Install LangChain and LangGraph
- Configure API keys
- Verify installation

## Duration

30 minutes

---

## Step 1: Create Virtual Environment

```bash
# Navigate to lab directory
cd LANGREF-100-Essentials/labs/Lab1

# Create virtual environment
python3 -m venv venv

# Activate (macOS/Linux)
source venv/bin/activate

# Activate (Windows)
venv\Scripts\activate
```

---

## Step 2: Install Dependencies

Create `requirements.txt`:

```txt
langchain>=0.1.0
langgraph>=0.0.20
langchain-core>=0.1.0
python-dotenv>=1.0.0
```

Install:

```bash
pip install -r requirements.txt
```

---

## Step 3: Configure API Keys

Create `.env` file:

```bash
# At project root (LANGREF-100-Essentials/.env)
DEEPSEEK_API_KEY=your_key_here
MINIMAX_API_KEY=your_key_here
OPENAI_API_KEY=your_key_here
```

---

## Step 4: Verify Installation

Create `verify.py`:

```python
"""Verify LangGraph installation."""
import langchain
import langgraph

print(f"LangChain: {langchain.__version__}")
print(f"LangGraph: {langgraph.__version__}")

# Test basic import
from langgraph.graph import StateGraph
print("✓ StateGraph imported successfully")

# Test state
from typing import TypedDict

class GraphState(TypedDict):
    messages: list

graph = StateGraph(GraphState)
print("✓ StateGraph created successfully")

print("\n✓ All checks passed!")
```

Run:

```bash
python verify.py
```

---

## Step 5: Test LangGraph API

Create `test_basic.py`:

```python
"""Basic LangGraph test."""
from typing import TypedDict
from langgraph.graph import StateGraph, END

# Define state
class MyState(TypedDict):
    value: int

# Create graph
graph = StateGraph(MyState)

# Add node
def increment(state: MyState) -> MyState:
    return {"value": state["value"] + 1}

graph.add_node("increment", increment)

# Set entry point
graph.set_entry_point("increment")

# Add edge to end
graph.add_edge("increment", END)

# Compile
app = graph.compile()

# Run
result = app.invoke({"value": 0})
print(f"Result: {result}")

print("\n✓ LangGraph working!")
```

Run:

```bash
python test_basic.py
```

---

## Troubleshooting

### ImportError: No module named 'langgraph'

```bash
pip install langgraph --upgrade
```

### API Key Error

Ensure `.env` file is in the project root and properly formatted.

---

## Exercises

### Exercise 1.1: Different State Types
Create a state with multiple types: `{"name": str, "age": int, "active": bool}`

### Exercise 1.2: Multiple Nodes
Add two nodes to a graph and connect them.

---

## Summary

✓ Created virtual environment  
✓ Installed LangChain/LangGraph  
✓ Configured API keys  
✓ Verified installation  

---

## Next Lab

[Lab 2: State & Nodes](../Lab2/README.md)
