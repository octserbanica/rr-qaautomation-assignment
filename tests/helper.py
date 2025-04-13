import requests
import logging
from bs4 import BeautifulSoup
from requests.auth import HTTPBasicAuth

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def login_user(base_url, username, password):
    login_url = f"{base_url}/login.htm"
    payload = {"username": username, "password": password}
    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    response = requests.post(login_url, data=payload, headers=headers)
    logging.info(f"Login request sent for user: {username}")

    assert response.status_code == 200, f"Expected status 200, got {response.status_code}"
    logging.info("Login response status code is 200")

    assert "Welcome" in response.text or "Accounts Overview" in response.text, "Login failed or unexpected response."
    logging.info("Login response content is valid")

    return response

def check_total_balance(base_url, user_data):
    username = user_data["username"]
    password = user_data["password"]
    customer_id = user_data["customer_id"]

    response = requests.get(
        f"{base_url}/services_proxy/bank/customers/{customer_id}/accounts",
        auth=HTTPBasicAuth(username, password))
    assert response.status_code == 200, "Failed to fetch account list."
    logging.info("Fetched account list successfully")

    total_balance = sum(float(acc.get("balance", 0)) for acc in response.json())
    logging.info(f"Total balance is: {total_balance:.2f}")

    assert total_balance >= 0, "Total amount should be positive"
    logging.info("Total balance is positive")
    return total_balance

def get_list_of_services(base_url):
    response = requests.get(f"{base_url}/services")
    assert response.status_code == 200, "Failed to fetch services page."
    logging.info("Services page fetched successfully")

    soup = BeautifulSoup(response.text, "html.parser")
    ports = {pt.get_text(strip=True) for pt in soup.find_all("span", class_="porttypename")}
    logging.info(f"Available services: {ports}")
    return list(ports)




