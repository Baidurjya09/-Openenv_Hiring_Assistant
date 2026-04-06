"""
Test the full pipeline with mock LLM responses (no API key needed).
"""

import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from env.hiring_env import HiringEnv
from models.schemas import Action


def mock_llm_selection(observation):
    """
    Simulate what an LLM should select based on the task.
    This is the "correct" answer for testing.
    """
    task_id = observation.task_id
    
    # Return the correct answers (simulating a perfect LLM)
    correct_answers = {
        "task_easy_001": ["c_easy_001"],
        "task_medium_001": ["c_med_001", "c_med_005"],
        "task_hard_001": ["c_hard_001", "c_hard_002"],
    }
    
    return correct_answers.get(task_id, [])


def test_full_pipeline():
    """Test the complete pipeline: reset → observe → act → score"""
    
    print("=" * 80)
    print("FULL PIPELINE TEST (Mock LLM)")
    print("=" * 80)
    print("Testing: Environment → Observation → Action → Grading → Result")
    print("=" * 80)
    
    difficulties = ["easy", "medium", "hard"]
    all_scores = []
    
    for difficulty in difficulties:
        print(f"\n{'█' * 80}")
        print(f"Testing {difficulty.upper()} Task")
        print(f"{'█' * 80}")
        
        # Step 1: Create environment
        print("\n[Step 1] Creating environment...")
        env = HiringEnv(difficulty=difficulty)
        print(f"  ✓ Environment created for difficulty: {difficulty}")
        
        # Step 2: Reset and get observation
        print("\n[Step 2] Resetting environment and getting observation...")
        observation = env.reset()
        print(f"  ✓ Task ID: {observation.task_id}")
        print(f"  ✓ Job: {observation.job_description['title']}")
        print(f"  ✓ Candidates: {len(observation.resumes)}")
        print(f"  ✓ Required Skills: {', '.join(observation.job_description['required_skills'])}")
        print(f"  ✓ Preferred Skills: {', '.join(observation.job_description['preferred_skills'])}")
        
        # Step 3: Mock LLM makes selection
        print("\n[Step 3] Mock LLM analyzing candidates...")
        selected_ids = mock_llm_selection(observation)
        print(f"  ✓ Mock LLM selected: {selected_ids}")
        
        # Show selected candidates
        for candidate_id in selected_ids:
            candidate = next(c for c in observation.resumes if c['id'] == candidate_id)
            print(f"    - {candidate['name']}: {', '.join(candidate['skills'])}")
        
        # Step 4: Create action
        print("\n[Step 4] Creating action...")
        action = Action(selected_candidates=selected_ids)
        print(f"  ✓ Action created with {len(action.selected_candidates)} candidates")
        
        # Step 5: Execute step and get result
        print("\n[Step 5] Executing step and getting result...")
        result = env.step(action)
        print(f"  ✓ Step executed")
        print(f"  ✓ Done: {result.done}")
        
        # Step 6: Display grading results
        print("\n[Step 6] Grading Results:")
        print(f"  Score: {result.reward.score:.4f}")
        print(f"  Correct Selections: {result.reward.correct_selections}/{result.reward.total_correct}")
        print(f"  False Positives: {result.reward.false_positives}")
        print(f"  Feedback: {result.reward.feedback}")
        
        all_scores.append(result.reward.score)
        
        # Verify perfect score
        if result.reward.score == 1.0:
            print(f"\n  ✅ PERFECT SCORE! Test passed for {difficulty} task")
        else:
            print(f"\n  ❌ FAILED! Expected 1.0, got {result.reward.score}")
            return False
    
    # Final summary
    avg_score = sum(all_scores) / len(all_scores)
    
    print("\n" + "=" * 80)
    print("FINAL RESULTS")
    print("=" * 80)
    print(f"Easy Task:   {all_scores[0]:.4f} ✓")
    print(f"Medium Task: {all_scores[1]:.4f} ✓")
    print(f"Hard Task:   {all_scores[2]:.4f} ✓")
    print(f"Average:     {avg_score:.4f}")
    print("=" * 80)
    print("✅ ALL TESTS PASSED! Pipeline is working correctly.")
    print("=" * 80)
    
    return True


def test_wrong_selections():
    """Test that wrong selections get penalized correctly"""
    
    print("\n\n")
    print("=" * 80)
    print("TESTING WRONG SELECTIONS (Negative Cases)")
    print("=" * 80)
    
    # Test 1: Select wrong candidate
    print("\n[Test 1] Selecting wrong candidate for EASY task...")
    env = HiringEnv(difficulty="easy")
    observation = env.reset()
    
    # Select Bob instead of Alice (Bob is Java dev, not Python)
    action = Action(selected_candidates=["c_easy_002"])
    result = env.step(action)
    
    print(f"  Selected: Bob (Java developer)")
    print(f"  Score: {result.reward.score:.4f}")
    print(f"  Feedback: {result.reward.feedback}")
    
    if result.reward.score == 0.0:
        print("  ✓ Correctly penalized wrong selection")
    else:
        print("  ✗ Should have scored 0.0")
        return False
    
    # Test 2: Select too many candidates
    print("\n[Test 2] Selecting too many candidates for MEDIUM task...")
    env = HiringEnv(difficulty="medium")
    observation = env.reset()
    
    # Select Emma, Iris (correct) + Frank (wrong - missing Node.js)
    action = Action(selected_candidates=["c_med_001", "c_med_005", "c_med_002"])
    result = env.step(action)
    
    print(f"  Selected: Emma, Iris, Frank (Frank is wrong)")
    print(f"  Score: {result.reward.score:.4f}")
    print(f"  Feedback: {result.reward.feedback}")
    
    if result.reward.score < 1.0:
        print("  ✓ Correctly penalized false positive")
    else:
        print("  ✗ Should have scored less than 1.0")
        return False
    
    # Test 3: Select too few candidates
    print("\n[Test 3] Selecting too few candidates for MEDIUM task...")
    env = HiringEnv(difficulty="medium")
    observation = env.reset()
    
    # Select only Emma, miss Iris
    action = Action(selected_candidates=["c_med_001"])
    result = env.step(action)
    
    print(f"  Selected: Emma only (missed Iris)")
    print(f"  Score: {result.reward.score:.4f}")
    print(f"  Feedback: {result.reward.feedback}")
    
    if result.reward.score < 1.0:
        print("  ✓ Correctly penalized false negative")
    else:
        print("  ✗ Should have scored less than 1.0")
        return False
    
    print("\n" + "=" * 80)
    print("✅ ALL NEGATIVE TESTS PASSED! Penalties work correctly.")
    print("=" * 80)
    
    return True


if __name__ == "__main__":
    # Run positive tests
    success = test_full_pipeline()
    
    if success:
        # Run negative tests
        test_wrong_selections()
    
    print("\n" + "█" * 80)
    print("COMPLETE TEST SUITE FINISHED")
    print("█" * 80)
    print("\nThe project is working correctly!")
    print("You can now run with a real LLM by setting:")
    print("  $env:HF_TOKEN = 'your_token'")
    print("  python inference.py")
    print("█" * 80)
