

def manager_menu():
    while True:
        print("\n-- Manager --\n")
        print("1. Add product")
        print("2. Add Staff")
        print("3. Make a Purchase")
        print("4. View Profile")
        print("5. Edit Product")
        print("6. Remove Product")
        print("7. View Products")
        print("8. View Sales")
        print("9. Return to Main Menu")

        try:
            option = int(input("\nChoose an Option: "))

            if option == 1:
                # Add product 
                ...

            elif option == 2:
                # Add Staff
                ...

            elif option == 3:
                # Make a purchase
                ...

            elif option == 4:
                # View Profile (either user/other users)
                ...

            elif option == 5:
                # Edit product
                ...

            elif option == 6:
                # Remove product
                ...

            elif option == 7:
                # View Products
                ...

            elif option == 8:
                # View Sales
                ...

            elif option == 9:
                print("Returning to Main menu")
                break

            else:
                print("[SYSTEM]     Invalid Option! Choose a valid option.")

        except ValueError as e:
            print(f"[SYSTEM]     Encountered input Error: {e}")

def cashier_menu():
    while True:
        print("\n-- Staff --\n")
        print("1. View Products")
        print("2. Make a Purchase")
        print("3. View User Profile")
        print("4. Return to Main Menu")

        try:
            option = int(input("\nChoose an Option: "))

            if option == 1:
                # View Products
                ...

            elif option == 2:
                # Start Transaction
                ...

            elif option == 3:
                # View User Profile
                ...

            elif option == 4:
                print("Returning to Main Menu")

            else:
                print("[SYSTEM]     Invalid Option. Choose a Valid option..")

        except ValueError as e:
            print(f"[SYSTEM]     Encountered input Error: {e}")
        