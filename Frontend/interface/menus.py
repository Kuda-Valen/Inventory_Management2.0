from services.add_product import add_product

def manager_menu():
    while True:
        print("\n-- Manager --\n")
        print("1. Product Menu") # -> View Products, Edit product, Remove product
        print("2. Start Transaction")
        print("3. Staff") # -> Add staff, view staff profiles
        print("4. Reports") # -> View Daily reports, Employee reports, monthly reports
        print("5. Profile")
        print("6. Return to Main Menu")

        try:
            option = int(input("\nChoose an Option: "))

            if option == 1:
                while True:
                    print("\n-- Products --\n")
                    print("1. Add Product")
                    print("2. View Products")
                    print("3. Edit Product")
                    print("4. Remove Product")
                    print("5. Return to Manager Menu")

                    try:
                        option = int(input("\nChoose an Option: "))

                        if option == 1:
                            add_product()

                        elif option == 2:
                            # View products
                            ...

                        elif option == 3:
                            # Edit product
                            ...

                        elif option == 4:
                            # Remove Product
                            ...

                        elif option == 5:
                            print("Returning..")
                            break

                        else:
                            print("\nInvalid Option. Choose a Valid option!!")

                    except ValueError as e:
                        print(f"\nEncountered Input Error: {e}")

            elif option == 2:
                # Start Transaction
                ...

            elif option == 3:
                while True:
                    print("\n-- Staff --\n")
                    print("1. Add Staff")
                    print("2. View Staff Stats")
                    print("3. Remove Staff")
                    print("4. Return")

                    try:
                        option = int(input("\nChoose Option: "))

                        if option == 1:
                            # Add Staff
                            ...

                        elif option == 2:
                            # View Staff Stats
                            ...

                        elif option == 3:
                            # Remove Staff 
                            ...

                        elif option == 4:
                            print("\nReturning..")
                            break

                        else:
                            print("\nInvalid option. Choose a Valid Option!!")

                    except ValueError as e:
                        print(f"\nEncountered Input Error: {e}")

            elif option == 4:
                while True:
                    print("\n-- Reports --\n")
                    print("1. Daily Report")
                    print("2. Staff Report")
                    print("3. Monthly Report")
                    print("4. Product Report")
                    print("5. Return")

                    try:
                        option = int(input("\nChoose Option: "))

                        if option == 1:
                            # Daily Report
                            ...

                        elif option == 2:
                            # Staff Report
                            ...

                        elif option == 3:
                            # Monthly Report
                            ...

                        elif option == 4:
                            # Product Report
                            ...

                        elif option == 5:
                            print("\nReturning...")
                            break

                        else:
                            print("\nInvalid Option. Choose a Valid Option!!")

                    except ValueError as e:
                        print(f"\nEncontered Input Error: {e}")

            elif option == 5:
                # View Profile
                ...

            elif option == 6:
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
        print("2. Start Transaction")
        print("3. Profile")
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
                break

            else:
                print("[SYSTEM]     Invalid Option. Choose a Valid option..")

        except ValueError as e:
            print(f"[SYSTEM]     Encountered input Error: {e}")
        