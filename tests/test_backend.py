import requests
import json

BASE_URL = "https://cosmicapp-app.kindflower-34fe9cb7.eastus.azurecontainerapps.io"

def signup(email, password):
    print(f"Attempting to sign up user: {email}")
    response = requests.post(f"{BASE_URL}/api/v1/signup", json={"email": email, "password": password})
    print(f"Signup response status: {response.status_code}")
    print(f"Signup response body: {response.json()}")
    response.raise_for_status()
    return response.json()

def login(email, password):
    print(f"Attempting to log in user: {email}")
    response = requests.post(
        f"{BASE_URL}/api/v1/login",
        data={"username": email, "password": password},
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    print(f"Login response status: {response.status_code}")
    print(f"Login response body: {response.json()}")
    response.raise_for_status()
    return response.json()

def get_me(token):
    print("Attempting to get current user info")
    response = requests.get(
        f"{BASE_URL}/api/v1/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    print(f"Get /me response status: {response.status_code}")
    print(f"Get /me response body: {response.json()}")
    response.raise_for_status()
    return response.json()

def create_chat_session(token):
    print("Attempting to create chat session")
    response = requests.post(
        f"{BASE_URL}/api/v1/sessions",
        headers={"Authorization": f"Bearer {token}"}
    )
    print(f"Create chat session response status: {response.status_code}")
    print(f"Create chat session response body: {response.json()}")
    response.raise_for_status()
    return response.json()

def send_message(token, session_id, message_content):
    print(f"Attempting to send message to session {session_id}")
    response = requests.post(
        f"{BASE_URL}/api/v1/sessions/{session_id}/messages",
        json={"content": message_content},
        headers={"Authorization": f"Bearer {token}"}
    )
    print(f"Send message response status: {response.status_code}")
    print(f"Send message response body: {response.json()}")
    response.raise_for_status()
    return response.json()

def get_messages(token, session_id):
    print(f"Attempting to get messages for session {session_id}")
    response = requests.get(
        f"{BASE_URL}/api/v1/sessions/{session_id}/messages",
        headers={"Authorization": f"Bearer {token}"}
    )
    print(f"Get messages response status: {response.status_code}")
    print(f"Get messages response body: {response.json()}")
    response.raise_for_status()
    return response.json()

def delete_chat_session(token, session_id):
    print(f"Attempting to delete chat session {session_id}")
    response = requests.delete(
        f"{BASE_URL}/api/v1/sessions/{session_id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    print(f"Delete chat session response status: {response.status_code}")
    print(f"Delete chat session response body: {response.json()}")
    response.raise_for_status()
    return response.json()

def delete_account(token):
    print("Attempting to delete user account")
    response = requests.delete(
        f"{BASE_URL}/api/v1/account",
        headers={"Authorization": f"Bearer {token}"}
    )
    print(f"Delete account response status: {response.status_code}")
    print(f"Delete account response body: {response.json()}")
    response.raise_for_status()
    return response.json()

def run_tests():
    test_email = "shubhambhiwapurkar@gmail.com"
    test_password = "123456789"

    try:
        # 1. Signup
        signup_response = signup(test_email, test_password)
        access_token = signup_response["access_token"]
        refresh_token = signup_response["refresh_token"]
        print("Signup successful.")

        # 2. Get /me
        get_me(access_token)
        print("Get /me successful.")

        # 3. Create chat session
        session_response = create_chat_session(access_token)
        session_id = session_response["id"]
        print(f"Chat session created with ID: {session_id}")

        # 4. Send message
        send_message(access_token, session_id, "Hello, this is a test message.")
        print("Message sent successfully.")

        # 5. Get messages
        messages = get_messages(access_token, session_id)
        print("Messages retrieved successfully:")
        for msg in messages:
            print(f"- {msg['content']}")

        # 6. Delete chat session
        delete_chat_session(access_token, session_id)
        print(f"Chat session {session_id} deleted successfully.")

        # 7. Delete account
        delete_account(access_token)
        print("Account deleted successfully.")

        print("\nAll tests passed!")

    except requests.exceptions.HTTPError as e:
        print(f"\nTest failed due to HTTP error: {e}")
        if e.response is not None:
            print(f"Response content: {e.response.text}")
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")

if __name__ == "__main__":
    run_tests()