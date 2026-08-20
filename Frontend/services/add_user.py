

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

