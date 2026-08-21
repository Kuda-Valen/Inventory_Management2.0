import requests

API_URL = "http://127.0.0.1:8000"

def login():
    print("\n-- Login Screen --\n")
    email = input("Enter Email: ").strip()
    password = input("Enter Password: ").strip()

    payload = {
        "email": email,
        "password": password
    }

    try:
        response = requests.post(f"{API_URL}/login/", json=payload)
        if response.status_code == 200:
            data = response.json()
            token = data['access_token']
            print(f"\nLogin Successful!")
            print(f"Logged in as: {data['email']} | {data['role']}")

            #return token, data
            return data

        else:
            error_detail = response.json().get("detail", "Login failed")
            print(f"\nError ({response.status_code}): {error_detail}")
            
    except requests.exceptions.ConnectionError:
        print("\nError: Could not connect to backend server. Make sure Uvicorn is running.")