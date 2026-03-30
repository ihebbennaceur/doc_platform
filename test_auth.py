import requests
import json
import time

time.sleep(2)  # Wait for server to start

base_url = "http://localhost:8000"

# Test registration
print("=" * 60)
print("Testing Registration")
print("=" * 60)

reg_data = {
    "email": "testuser456@example.com",
    "password": "SecurePassword1234"
}

try:
    response = requests.post(
        f"{base_url}/api/register/",
        json=reg_data,
        headers={"Content-Type": "application/json"}
    )
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
except Exception as e:
    print(f"Error: {e}")

print("\n" + "=" * 60)
print("Testing Login")
print("=" * 60)

login_data = {
    "email": "testuser456@example.com",
    "password": "SecurePassword1234"
}

try:
    response = requests.post(
        f"{base_url}/api/login/",
        json=login_data,
        headers={"Content-Type": "application/json"}
    )
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
except Exception as e:
    print(f"Error: {e}")
