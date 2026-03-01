# Lab 5: Production Patterns

## Objectives

- Error handling
- Logging and monitoring
- Configuration management
- Deployment best practices

## Duration

60 minutes

---

## Error Handling

### Try/Catch in Nodes

```python
def safe_node(state: AgentState) -> AgentState:
    try:
        # Risky operation
        result = api.call()
        return {"data": result}
    except APIError as e:
        return {"error": str(e), "status": "failed"}
```

### Retry Logic

```python
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=1, max=10))
def reliable_api_call():
    return api.call()
```

---

## Logging

### Structured Logging

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger("langgraph")

def monitored_node(state: AgentState) -> AgentState:
    logger.info(f"Processing node with state: {state}")
    try:
        result = process(state)
        logger.info("Node completed successfully")
        return result
    except Exception as e:
        logger.error(f"Node failed: {e}")
        raise
```

---

## Configuration

### Environment-Based Config

```python
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    API_KEY = os.getenv("API_KEY")
    DB_PATH = os.getenv("DB_PATH", "default.db")
    MAX_RETRIES = int(os.getenv("MAX_RETRIES", "3"))
    TIMEOUT = int(os.getenv("TIMEOUT", "30"))
```

---

## Health Checks

```python
def health_check():
    """Verify graph is ready."""
    try:
        # Test basic invocation
        result = app.invoke({"test": True})
        return {"status": "healthy", "result": result}
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}
```

---

## Deployment Checklist

- [ ] Error handling in all nodes
- [ ] Logging configured
- [ ] Environment variables for secrets
- [ ] Health check endpoint
- [ ] Rate limiting
- [ ] Monitoring/alerting
- [ ] Graceful shutdown
- [ ] Resource limits

---

## Exercises

### Exercise 5.1: Error Handling
Add error handling to Lab 4 counter that:
- Catches API/timeouts
- Logs errors
- Returns graceful failure

### Exercise 5.2: Logging System
Implement structured logging:
- Per-node logging
- Error tracking
- Performance metrics

### Exercise 5.3: Health Endpoint
Create Flask/FastAPI endpoint that:
- Returns graph status
- Shows last run result
- Reports any errors

---

## Summary

✓ Added error handling  
✓ Configured logging  
✓ Built configuration system  
✓ Created health checks  

---

## Course Complete!

🎉 Congratulations!

You've completed LangGraph 100 Essentials!

---

## Next Steps

- Build production applications
- Explore advanced patterns
- Contribute to LangGraph
- Create your own courses!
