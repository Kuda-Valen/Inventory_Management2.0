import typer
import requests

app = typer.Typer(help="Backend Admin CLI for Inventory Management System")
API_URL = "http://127.0.0.1:8000"

@app.commands()
def create(first_name: str, last_name: str, email: str, phone: str, role: str, password: str):
    payload = {
        "first_name": first_name,
        "last_name": last_name,
        "email": email,
        "phone": phone,
        "role": role,
        "password": password
    }
    try:
        response = requests.post(f"{API_URL}/employees/", json=payload)
        if response.status_code == 200:
            data = response.json()
            typer.echo(f"Success: Employee Created with ID {data['employee_id']}")

        else:
            typer.echo(f"Error ({response.status_code}): {response.json().get('detail', response.text)}")

    except requests.exceptions.ConnectionError:
        typer.echo("Error: Could not connect to FastAPI server. Ensure Uvicorn is running.")

if __name__ == "__main__":
    app()