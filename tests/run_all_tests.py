import os
import sys
import pytest
from dotenv import dotenv_values

# Add the project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Load environment variables from cosmotalks/app/.env
env_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'app', '.env'))
if os.path.exists(env_path):
    config = dotenv_values(env_path)
    for key, value in config.items():
        os.environ[key] = value
else:
    print(f"Warning: .env file not found at {env_path}. Tests might fail due to missing environment variables.")

print("Running backend integration tests...")
try:
    from tests.test_backend import run_tests as run_backend_tests
    run_backend_tests()
    print("\nBackend integration tests completed successfully.")
except Exception as e:
    print(f"\nBackend integration tests failed: {e}")
    sys.exit(1)

print("\nRunning authentication unit tests...")
try:
    # Pytest will handle its own output, we just need to run it.
    # The -s flag allows stdout to be captured.
    # The -q flag makes the output quieter.
    # The --tb=no flag removes traceback information for cleaner output on success.
    pytest.main(["tests/test_auth.py", "-s", "-q", "--tb=no"])
    print("\nAuthentication unit tests completed successfully.")
except Exception as e:
    print(f"\nAuthentication unit tests failed: {e}")
    sys.exit(1)

print("\nAll tests finished.")