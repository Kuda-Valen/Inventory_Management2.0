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