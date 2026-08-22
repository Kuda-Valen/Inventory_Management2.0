import requests

API_URL = "http://127.0.0.1:8000"

def start_transaction(jwt_token: str, employee_id: int):
    print("\n== START NEW TRANSACTION ==\n")
    headers = {"Authorization": f"Bearer {jwt_token}"}
    cart = []

    while True:
        try:
            prod_id_input = input("Enter Product ID to add (or type 'done' to checkout): ").strip()
            if prod_id_input.lower() == 'done':
                break

            prod_id = int(prod_id_input)
            quantity = int(input("Enter Quantity: "))
            cart.append({"product_id": prod_id, "quantity": quantity})
            print(f"Added Product ID {prod_id} (x{quantity} to cart.)")

        except ValueError:
            print("Invalid input. Please enter numbers for ID and Quantity.")

    if not cart:
        print("Transaction canceled: Cart is empty.")
        return

    customer_id = None
    has_customer = input("\nAttach Customer to transaction? (y/n): ").strip().lower()

    if has_customer == 'y':
        cust_input = input("Enter Customer ID: ").strip()
        if cust_input.isdigit():
            customer_id = int(cust_input)

    print("\nSelect Payment Method:")
    print("1. Cash\n2. Card\n3. EFT")
    pm_choice = input("OPtion (1-3): ").strip()
    payment_methods = {"1": "CASH", "2": "CARD", "3": "EFT"}
    payment_method = payment_methods.get(pm_choice, "CASH")

    payload = {
        "customer_id": customer_id,
        "payment_method": payment_method,
        "items": cart
    }

    try:
        response = requests.post(f"{API_URL}/orders/checkout/", json=payload, headers=headers)
        if response.status_code == 201:
            receipt = response.json()
            print("\n==================================")
            print("     TRANSACTION SUCCESSFUL!")
            print(f"     Receipt #: {receipt['receipt_number']}")
            print(f"     Total Paid: R{receipt['total_amount']:.2f}")
            print(f"     Payment Method: {receipt['payment_method']}")
            print("==================================")

        else:
            error = response.json().get("detail", "Checkout Failed")
            print(f"\nTransaction Error ({response.status_code}): {error}")

    except requests.exceptions.ConnectionError:
        print("\nError: Could not connect to backend server.")