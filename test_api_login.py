import requests

def test_api_login():
    url = "http://localhost:8000/api/v1/login/access-token"
    payload = {
        "username": "user@demo.com",
        "password": "password123"
    }
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    
    try:
        response = requests.post(url, data=payload, headers=headers)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
    except Exception as e:
        print(f"Connection Error: {e}")

if __name__ == "__main__":
    test_api_login()
