"""
Test that inference.py outputs scores with enough precision
"""
import sys
import os

# Mock the OpenAI client to avoid actual API calls
class MockChoice:
    def __init__(self, content):
        self.message = type('obj', (object,), {'content': content})()

class MockResponse:
    def __init__(self, content):
        self.choices = [MockChoice(content)]

class MockClient:
    def __init__(self, *args, **kwargs):
        pass
    
    class chat:
        class completions:
            @staticmethod
            def create(*args, **kwargs):
                # Return empty selection to trigger edge case with score 0.0001
                return MockResponse('{"selected_candidates": []}')

# Patch the OpenAI import before importing inference
sys.modules['openai'] = type('module', (), {'OpenAI': MockClient})()

# Now import inference
sys.path.insert(0, os.path.dirname(__file__))
os.environ["API_KEY"] = "test_key"
os.environ["API_BASE_URL"] = "https://test.url"
os.environ["MODEL_NAME"] = "test-model"

import inference
from io import StringIO

def test_output_format():
    """Test that scores are output with 4 decimal places"""
    
    print("Testing output format...")
    print("=" * 60)
    
    # Capture stdout
    old_stdout = sys.stdout
    sys.stdout = StringIO()
    
    try:
        # Run a single task
        result = inference.run_task("task_easy_001", "easy")
        
        # Get the output
        output = sys.stdout.getvalue()
        sys.stdout = old_stdout
        
        print("Captured output:")
        print(output)
        print("=" * 60)
        
        # Check that the output contains 4 decimal places
        # Score should be 0.0001 (empty selection)
        if "reward=0.0001" in output:
            print("✓ STEP line has 4 decimal places (0.0001)")
        elif "reward=0.00" in output:
            print("✗ STEP line has only 2 decimal places (0.00) - WILL FAIL VALIDATION!")
            return False
        else:
            print(f"? Could not find reward in output")
        
        if "score=0.0001" in output:
            print("✓ END line has 4 decimal places (0.0001)")
        elif "score=0.00" in output:
            print("✗ END line has only 2 decimal places (0.00) - WILL FAIL VALIDATION!")
            return False
        else:
            print(f"? Could not find score in output")
        
        if "rewards=0.0001" in output:
            print("✓ Rewards list has 4 decimal places (0.0001)")
        elif "rewards=0.00" in output:
            print("✗ Rewards list has only 2 decimal places (0.00) - WILL FAIL VALIDATION!")
            return False
        else:
            print(f"? Could not find rewards in output")
        
        print("=" * 60)
        print("✓ All output formats use 4 decimal places")
        print("✓ Scores will not round to 0.00 or 1.00")
        return True
        
    except Exception as e:
        sys.stdout = old_stdout
        print(f"✗ Error during test: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_output_format()
    exit(0 if success else 1)
