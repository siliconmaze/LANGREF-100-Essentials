#!/usr/bin/env python3
"""
Lab 3 Solution: Conditional Edges
=================================
"""

from typing import TypedDict
from langgraph.graph import StateGraph, END

class GradeState(TypedDict):
    score: int
    grade: str
    feedback: str

def grade_a(state: GradeState) -> GradeState:
    return {"grade": "A", "feedback": "Excellent work!"}

def grade_b(state: GradeState) -> GradeState:
    return {"grade": "B", "feedback": "Good job!"}

def grade_c(state: GradeState) -> GradeState:
    return {"grade": "C", "feedback": "Fair effort."}

def grade_f(state: GradeState) -> GradeState:
    return {"grade": "F", "feedback": "Needs improvement."}

def classify_grade(state: GradeState) -> str:
    score = state["score"]
    if score >= 90:
        return "grade_a"
    elif score >= 80:
        return "grade_b"
    elif score >= 70:
        return "grade_c"
    else:
        return "grade_f"

def main():
    print("=" * 50)
    print("Lab 3: Conditional Edges")
    print("=" * 50)
    
    # Test scores
    test_scores = [95, 85, 75, 65]
    
    for score in test_scores:
        # Build fresh graph for each test
        graph = StateGraph(GradeState)
        
        graph.add_node("grade_a", grade_a)
        graph.add_node("grade_b", grade_b)
        graph.add_node("grade_c", grade_c)
        graph.add_node("grade_f", grade_f)
        
        graph.set_entry_point("grade_a")
        
        # Add conditional edges from grade_a (all routes go through classifier)
        graph.add_conditional_edges(
            "grade_a",
            classify_grade,
            {
                "grade_a": "grade_a",
                "grade_b": "grade_b", 
                "grade_c": "grade_c",
                "grade_f": "grade_f"
            }
        )
        
        # All lead to END
        graph.add_edge("grade_a", END)
        graph.add_edge("grade_b", END)
        graph.add_edge("grade_c", END)
        graph.add_edge("grade_f", END)
        
        app = graph.compile()
        result = app.invoke({"score": score, "grade": "", "feedback": ""})
        
        print(f"\nInput score: {score}")
        print(f"Output: grade={result['grade']}, feedback={result['feedback']}")
    
    print("\n✓ Lab 3 Complete!")
    return True

if __name__ == "__main__":
    main()
