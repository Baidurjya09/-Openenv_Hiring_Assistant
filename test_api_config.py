"""
Test script to verify API configuration uses correct environment variables
"""
import os
import sys

def test_api_config():
    """Verify that inference.py uses API_KEY and API_BASE_URL correctly"""
    
    print("Testing API Configuration...")
    print("=" * 60)
    
    # Set test environment variables
    os.environ["API_KEY"] = "test_api_key_from_validator"
    os.environ["API_BASE_URL"] = "https://test.validator.url/v1"
    os.environ["MODEL_NAME"] = "test-model"
    
    # Clear HF_TOKEN to ensure API_KEY takes precedence
    if "HF_TOKEN" in os.environ:
        del os.environ["HF_TOKEN"]
    
    # Import inference module (this will initialize the client)
    sys.path.insert(0, os.path.dirname(__file__))
    import inference
    
    # Check that the correct values are being used
    print(f"API_KEY:      {inference.API_KEY}")
    print(f"API_BASE_URL: {inference.API_BASE_URL}")
    print(f"MODEL_NAME:   {inference.MODEL_NAME}")
    print("=" * 60)
    
    # Verify
    assert inference.API_KEY == "test_api_key_from_validator", \
        f"Expected API_KEY='test_api_key_from_validator', got '{inference.API_KEY}'"
    
    assert inference.API_BASE_URL == "https://test.validator.url/v1", \
        f"Expected API_BASE_URL='https://test.validator.url/v1', got '{inference.API_BASE_URL}'"
    
    assert inference.MODEL_NAME == "test-model", \
        f"Expected MODEL_NAME='test-model', got '{inference.MODEL_NAME}'"
    
    # Check that client is initialized with correct values
    assert inference.client.api_key == "test_api_key_from_validator", \
        "Client not initialized with correct API_KEY"
    
    # OpenAI client normalizes base_url, so check if it starts with the expected URL
    client_base_url = str(inference.client.base_url)
    expected_base = "https://test.validator.url/v1"
    assert client_base_url.startswith(expected_base) or client_base_url.rstrip('/') == expected_base, \
        f"Client not initialized with correct API_BASE_URL. Expected '{expected_base}', got '{client_base_url}'"
    
    print("✓ All checks passed!")
    print("✓ API_KEY environment variable is correctly used")
    print("✓ API_BASE_URL environment variable is correctly used")
    print("✓ OpenAI client is initialized with validator credentials")
    
    return True

if __name__ == "__main__":
    try:
        success = test_api_config()
        exit(0 if success else 1)
    except AssertionError as e:
        print(f"\n✗ Test failed: {e}")
        exit(1)
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        exit(1)
