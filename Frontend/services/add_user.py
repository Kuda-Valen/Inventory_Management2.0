import requests

API_URL = "http://127.0.0.1:8000"

def add_user():
    print("\n-- Add New User --\n")
    print("1. Add Employee")
    print("2. Add Customer")
    print("3. Return to Main Menu")

    try:
        option = int(input("\nChoose an Option: "))

        if option == 1:
            first_name = input("\nEnter First Name: ").strip().lower()
            last_name = input("Enter Last Name: ").strip().lower()
            email = input("Enter Email: ").strip().lower()
            phone = input("Enter Phone: ").strip()
            role = input("Choose Employee Role: [manager] or [cashier]").strip().lower()
            password = input("Enter Password").strip()

            payload = {
                "first_name": first_name,
                "last_name": last_name,
                "email": email,
                "phone": phone,
                "role": role,
                "password": password
            }
            try:
                response = requests.post(f"{API_URL}/add_employee/", json=payload)
                if response.status_code == 200:
                    data = response.json()
                    print(f"\nAccount created successfully! Welcome, {data['first_name']} with ID: {data['employee_id']}")

                else:
                    error_detail = response.json().get("detail", "Add Employee failed!")
                    print(f"\nError ({response.status_code}): {error_detail}")

            except requests.exceptions.ConnectionError:
                print("\nError: Could not connect to backend server. Make sure Uvicorn is running.")

        elif option == 2:
            first_name = input("\nEnter First Name: ")
            last_name = input("Enter Last Name: ")
            email = input("Enter Email: ")
            phone = input("Enter phone")

        elif option == 3:
            print("Returning to Main Menu")
            return

        else:
            print("[SYSTEM]     Invalid Optoin. Select Valid Option.")

    except ValueError as e:
        print(f"[SYSTEM]    Encountered Input Error: {e}")

