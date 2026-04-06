"""
Test script to verify the environment works without API calls.
"""

import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from env.hiring_env import HiringEnv
from models.schemas import Action

def test_environment():
    print("=" * 60)
    print("  Testing AI Hiring Assistant Environment")
    print("=" * 60)
    
    difficulties = ["easy", "medium", "hard"]
    
    for difficulty in difficulties:
        print(f"\n[Testing {difficulty.upper()} task]")
        
        # Create environment
        env = HiringEnv(difficulty=difficulty)
        
        # Reset and get observation
        observation = env.reset()
        
        print(f"  Job: {observation.job_description['title']}")
        print(f"  Required Skills: {', '.join(observation.job_description['required_skills'])}")
        print(f"  Candidates: {len(observation.resumes)}")
        
        # Get correct answer from state
        state = env.state()
        correct_ids = state['correct_candidate_ids']
        print(f"  Correct Answer: {correct_ids}")
        
        # Test with correct answer
        action = Action(selected_candidates=correct_ids)
        result = env.step(action)
        
        print(f"  Score: {result.reward.score:.4f}")
        print(f"  Feedback: {result.reward.feedback}")
        
        # Verify perfect score
        assert result.reward.score == 1.0, f"Expected perfect score for {difficulty}"
        print(f"  ✓ Test passed!")
    
    print("\n" + "=" * 60)
    print("  All tests passed successfully!")
    print("=" * 60)

if __name__ == "__main__":
    test_environment()
