"""
Test script to verify all scores are strictly between 0 and 1
"""
from graders.hiring_grader import HiringGrader

def test_score_ranges():
    grader = HiringGrader()
    
    test_cases = [
        # (selected, correct, description)
        ([], [], "Empty both"),
        ([], ["c1"], "Empty selection, has correct"),
        (["c1"], [], "Has selection, empty correct"),
        (["c1"], ["c1"], "Perfect match - single"),
        (["c1", "c2"], ["c1", "c2"], "Perfect match - multiple"),
        (["c1", "c2", "c3"], ["c1", "c2"], "All correct + false positive"),
        (["c1"], ["c1", "c2"], "Partial - missing one"),
        (["c1", "c3"], ["c1", "c2"], "Partial - one correct, one wrong"),
        (["c3"], ["c1", "c2"], "All wrong"),
    ]
    
    print("Testing score ranges...")
    print("=" * 60)
    
    all_valid = True
    for selected, correct, desc in test_cases:
        reward = grader.grade(selected, correct)
        score = reward.score
        
        is_valid = 0.0 < score < 1.0
        status = "✓" if is_valid else "✗"
        
        print(f"{status} {desc:40s} score={score:.4f}")
        
        if not is_valid:
            all_valid = False
            print(f"   ERROR: Score {score} is not strictly between 0 and 1!")
    
    print("=" * 60)
    if all_valid:
        print("✓ All scores are strictly between 0 and 1")
        return True
    else:
        print("✗ Some scores are out of range!")
        return False

if __name__ == "__main__":
    success = test_score_ranges()
    exit(0 if success else 1)
