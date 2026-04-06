"""
Test the grader with various scenarios.
"""

import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from graders.hiring_grader import HiringGrader

def test_grader():
    grader = HiringGrader()
    
    print("=" * 60)
    print("  Testing Hiring Grader")
    print("=" * 60)
    
    # Test 1: Perfect match
    print("\n[Test 1: Perfect match]")
    result = grader.grade(["c1", "c2"], ["c1", "c2"])
    print(f"  Selected: ['c1', 'c2'], Correct: ['c1', 'c2']")
    print(f"  Score: {result.score}, Feedback: {result.feedback}")
    assert result.score == 1.0
    
    # Test 2: Partial match
    print("\n[Test 2: Partial match - 1 of 2 correct]")
    result = grader.grade(["c1"], ["c1", "c2"])
    print(f"  Selected: ['c1'], Correct: ['c1', 'c2']")
    print(f"  Score: {result.score}, Feedback: {result.feedback}")
    
    # Test 3: False positive
    print("\n[Test 3: False positive]")
    result = grader.grade(["c1", "c2", "c3"], ["c1", "c2"])
    print(f"  Selected: ['c1', 'c2', 'c3'], Correct: ['c1', 'c2']")
    print(f"  Score: {result.score}, Feedback: {result.feedback}")
    
    # Test 4: Empty selection
    print("\n[Test 4: Empty selection]")
    result = grader.grade([], ["c1", "c2"])
    print(f"  Selected: [], Correct: ['c1', 'c2']")
    print(f"  Score: {result.score}, Feedback: {result.feedback}")
    assert result.score == 0.0
    
    # Test 5: Completely wrong
    print("\n[Test 5: Completely wrong]")
    result = grader.grade(["c3", "c4"], ["c1", "c2"])
    print(f"  Selected: ['c3', 'c4'], Correct: ['c1', 'c2']")
    print(f"  Score: {result.score}, Feedback: {result.feedback}")
    assert result.score == 0.0
    
    print("\n" + "=" * 60)
    print("  All grader tests passed!")
    print("=" * 60)

if __name__ == "__main__":
    test_grader()
