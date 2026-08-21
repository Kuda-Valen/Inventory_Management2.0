import requests

API_URL = "http://127.0.0.1:8000"

def add_product():
    print("\n-- Add Product --\n")
    product_name = input("Enter Product Name: ").strip().lower()
    description = input("Enter Description: ").strip().lower()
    cost_price = float(input("Enter Cost price: "))
    selling_price = float(input("Enter Selling Price: "))
    stock_quantity = int(input("Enter Quantity: "))
    reorder_level = int(input("Enter Reorder Level: "))

    payload = {
        "product_name": product_name,
        "description": description,
        "cost_price": cost_price,
        "selling_price": selling_price,
        "stock_quantity": stock_quantity,
        "reorder_level": reorder_level
    }

    try:
        response = requests.post(f"{API_URL}/add_product/", json=payload)
        if response.status_code == 200:
            data = response.json()
            print(f"\nProduct added successfully! \nProduct : '{data['product_name']}' | Product ID: '{data['product_id']}'")

        else:
            error_detail = response.json().get("detail", "Add New Product Failed!")
            print(f"\nError ({response.status_code}): {error_detail}")

    except requests.exceptions.ConnectionError:
        print("\nError: Could not connect to backend server. Make sure Uvicorn is running.")

def view_products():
    print("\n-- Products List --\n")
    try:
        response = requests.get(f"{API_URL}/products/")
        if response.status_code == 200:
            products = response.json()
            if not products:
                print("No Products found in inventory.")
                return

            print(f"{'ID':<5} | {'Product Name':<20} | {'Price (R)':<10} | {'Stock':<8} | {'Reorder Level':<12}")
            print("-" * 65)
            for item in products:
                print(
                    f"{item['product_id']:<5} | "
                    f"{item['product_name']:<20} | "
                    f"{item['selling_price']:<10.2f} | "
                    f"{item['stock_quantity']:<8} | "
                    f"{item['reorder_level']:<12}"
                )

        else:
            print(f"Error ({response.status_code}): {response.text}")

    except requests.exceptions.ConnectionError:
        print("\nError: Could not connect to backend server. Ensure Uvicorn is running.")

def add_stock():
    print("\nAdd Stock Coming soon..")
    

def edit_product():
    print("\nEdit Product coming soon...")

def remove_product():
    print("\nRemove Product coming soon..")

    