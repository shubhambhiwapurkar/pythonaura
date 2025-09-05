import requests
import json

BASE_URL = "https://cosmicapp-app.kindflower-34fe9cb7.eastus.azurecontainerapps.io"

def signup(email, password):
    signup_data = {
        "email": email,
        "password": password,
        "first_name": "Test2",
        "last_name": "User",
        "birth_details": {
            "date": "2000-01-01",
            "time": "12:00",
            "location": "New York, NY"
        }
    }
    response = requests.post(f"{BASE_URL}/api/v1/auth/signup", json=signup_data)
    response.raise_for_status()
    return response.json()

def login(email, password):
    response = requests.post(
        f"{BASE_URL}/api/v1/login",
        data={"username": email, "password": password},
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    response.raise_for_status()
    return response.json()

def create_chat_session(token):
    response = requests.post(
        f"{BASE_URL}/api/v1/chat/sessions",
        json={}, # Add an empty JSON body
        headers={"Authorization": f"Bearer {token}"}
    )
    response.raise_for_status()
    return response.json()

def send_message(token, session_id, message_content):
    response = requests.post(
        f"{BASE_URL}/api/v1/chat/sessions/{session_id}/messages",
        json={"content": message_content},
        headers={"Authorization": f"Bearer {token}"}
    )
    response.raise_for_status()
    return response.json()

def get_messages(token, session_id):
    response = requests.get(
        f"{BASE_URL}/api/v1/chat/sessions/{session_id}/messages",
        headers={"Authorization": f"Bearer {token}"}
    )
    response.raise_for_status()
    return response.json()

def delete_chat_session(token, session_id):
    response = requests.delete(
        f"{BASE_URL}/api/v1/chat/sessions/{session_id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    response.raise_for_status()
    return response.json()

def delete_account(token):
    response = requests.delete(
        f"{BASE_URL}/api/v1/account",
        headers={"Authorization": f"Bearer {token}"}
    )
    response.raise_for_status()
    return response.json()

def run_tests():
    test_email = "test_user4@example.com"
    test_password = "testpassword"

    try:
        # 1. Signup
        signup_response = signup(test_email, test_password)
        access_token = signup_response["access_token"]
        refresh_token = signup_response["refresh_token"]
        print(f"Signup Response: {signup_response}")

        # 2. Create chat session
        session_response = create_chat_session(access_token)
        session_id = session_response["id"]
        print(f"Create chat session Response: {session_response}")

        # 4. Send message
        send_message_response = send_message(access_token, session_id, "Hello, this is a test message.")
        print(f"Send message Response: {send_message_response}")

        # 5. Get messages
        messages = get_messages(access_token, session_id)
        print(f"Get messages Response: {messages}")

        # 6. Delete chat session
        delete_chat_session_response = delete_chat_session(access_token, session_id)
        print(f"Delete chat session Response: {delete_chat_session_response}")

        # 7. Delete account
        delete_account_response = delete_account(access_token)
        print(f"Delete account Response: {delete_account_response}")

        print("\nAll backend tests completed.")

    except requests.exceptions.HTTPError as e:
        print(f"\nBackend test failed due to HTTP error: {e}")
        if e.response is not None:
            print(f"Response content: {e.response.text}")
        raise # Re-raise to indicate failure
    except Exception as e:
        print(f"\nAn unexpected error occurred during backend tests: {e}")
        raise # Re-raise to indicate failure

if __name__ == "__main__":
    run_tests()