from interface.menus import manager_menu, cashier_menu
from services.add_user import add_user

if __name__ == "__main__":

    while True:
        print("\n==== Inventory Management System =====\n")
        print("1. Login")
        print("2. Add User")
        print("3. Exit")

        try:
            option = int(input("\nChoose an Option: "))

            if option == 1:
                # Authentication
                ...
            
            elif option == 2:
                # Add User
                add_user()

            elif option == 3:
                print("Exiting!!")
                break

            else:
                print("[SYSTEM]     Invalid Option. Choose a Valid option!!")
        except ValueError as e:
            print(f"[SYSTEM]    Encountered Input Error: {e}")