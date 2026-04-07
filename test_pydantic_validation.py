"""
Test Pydantic validation for Reward schema
"""
from models.schemas import Reward

def test_pydantic_validation():
    """Test that Pydantic accepts scores in valid range and rejects invalid ones"""
    
    print("Testing Pydantic Reward validation...")
    print("=" * 60)
    
    test_cases = [
        (0.0001, True, "Minimum valid score"),
        (0.5, True, "Middle score"),
        (0.9999, True, "Maximum valid score"),
        (0.0, False, "Exactly 0.0 (should fail)"),
        (1.0, False, "Exactly 1.0 (should fail)"),
        (-0.1, False, "Negative score (should fail)"),
        (1.1, False, "Above 1.0 (should fail)"),
    ]
    
    all_passed = True
    
    for score, should_pass, description in test_cases:
        try:
            reward = Reward(
                score=score,
                correct_selections=1,
                total_correct=2,
                false_positives=0,
                feedback="Test"
            )
            if should_pass:
                print(f"✓ {description:40s} score={score:.4f} - ACCEPTED")
            else:
                print(f"✗ {description:40s} score={score:.4f} - SHOULD HAVE BEEN REJECTED!")
                all_passed = False
        except Exception as e:
            if not should_pass:
                print(f"✓ {description:40s} score={score:.4f} - REJECTED (expected)")
            else:
                print(f"✗ {description:40s} score={score:.4f} - REJECTED (should pass!)")
                print(f"   Error: {e}")
                all_passed = False
    
    print("=" * 60)
    if all_passed:
        print("✓ All Pydantic validation tests passed")
        return True
    else:
        print("✗ Some Pydantic validation tests failed")
        return False

if __name__ == "__main__":
    success = test_pydantic_validation()
    exit(0 if success else 1)
