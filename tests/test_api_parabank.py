import logging
import requests
from helper import login_user, check_total_balance, get_list_of_services
from requests.auth import HTTPBasicAuth
import pytest

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

@pytest.mark.run(order =2)
def test_api_login_with_registered_user(user_data, base_url):
    """Test login with registered user using API."""
    response = login_user(base_url, user_data["username"], user_data["password"] )
    assert response.status_code == 200
    logging.info(f"Login request sent successfully")


@pytest.mark.run(order =3)
def test_create_savings(base_url, user_data):
    """Test creating a savings account."""
    username = user_data["username"]
    password = user_data["password"]
    customer_id = user_data["customer_id"]

    account_response = requests.get(
        f"{base_url}/services_proxy/bank/customers/{customer_id}/accounts",
        auth=HTTPBasicAuth(username, password))
    assert account_response.status_code == 200, "Failed to get account list."
    logging.info("Successfully fetched accounts for savings creation")

    account_id = account_response.json()[0]["id"]
    response = requests.post(
        f"{base_url}/services_proxy/bank/createAccount",
        params={"customerId": customer_id, "newAccountType": 1, "fromAccountId": account_id},
        auth=HTTPBasicAuth(username, password))
    assert response.status_code == 200, "Failed to create savings account."
    logging.info("Savings account created successfully")

@pytest.mark.run(order =4)
def test_check_total(base_url, user_data):
    """Test checking the total balance."""
    total = check_total_balance(base_url, user_data)
    assert total >=0
    logging.info("Total amount is more than 0")

@pytest.mark.run(order =5)
def test_check_products(base_url):
    """Test checking available products."""
    response = requests.get(f"{base_url}/products")
    assert response.status_code == 200, "Failed to fetch products page."
    logging.info("Products page fetched successfully")

@pytest.mark.run(order =6)
def test_get_list_services(base_url):
    """Test retrieving available services."""
    service_list = get_list_of_services(base_url)
    assert "Bookstore" in service_list
    logging.info("The website provides the Bookstore service")

@pytest.mark.run(order =7)
def test_create_loan_account(base_url, user_data, loan_data):
    """Test creating a loan account."""
    amount, down_payment = loan_data
    username = user_data["username"]
    password = user_data["password"]
    customer_id = user_data["customer_id"]

    response_before = requests.get(
        f"{base_url}/services_proxy/bank/customers/{customer_id}/accounts",
        auth=HTTPBasicAuth(username, password))
    assert response_before.status_code == 200, "Failed to get accounts before loan request."
    logging.info("Fetched accounts before loan request")

    account_ids_before = {acc["id"] for acc in response_before.json()}
    if not account_ids_before:
        raise Exception("No accounts available to create a loan from.")

    from_account_id = next(iter(account_ids_before))
    response_loan = requests.post(
        f"{base_url}/services_proxy/bank/requestLoan",
        params={"customerId": customer_id, "amount": amount, "downPayment": down_payment,
                "fromAccountId": from_account_id},
        auth=HTTPBasicAuth(username, password))
    assert response_loan.status_code == 200, "Loan creation failed."
    logging.info("Loan created successfully")

    response_after = requests.get(
        f"{base_url}/services_proxy/bank/customers/{customer_id}/accounts",
        auth=HTTPBasicAuth(username, password))
    assert response_after.status_code == 200, "Failed to get accounts after loan request."
    logging.info("Fetched accounts after loan request")

    new_accounts = [acc for acc in response_after.json() if acc["id"] not in account_ids_before]
    assert new_accounts, "No new account was created after loan request."
    logging.info("New account was successfully created")

    has_loan_account = any(acc.get("type") == "LOAN" or acc.get("type") == 3 for acc in new_accounts)
    assert has_loan_account, "New account is not of type LOAN."
    logging.info("Loan account verified in new accounts")

@pytest.mark.run(order =8)
def test_api_logout(base_url, user_data):
    """Test logging out using the API."""
    logout_url = f"{base_url}/logout.htm"
    response = requests.get(logout_url)
    assert response.status_code == 200, "Logout failed."
    logging.info("Logout successful")

@pytest.mark.run(order=9)
def test_clean_up(base_url):
    """Test cleaning up and reinitializing database."""
    admin_url = f"{base_url}/admin.htm"
    jms_shutdown= requests.post(f"{base_url}/jms.htm", data={"shutdown":"true"})
    assert jms_shutdown.status_code == 200
    logging.info("Request for JMS to shutdown is performed")
    shutdown = requests.get(f"{admin_url}?isJmsRunning=true&loanProviders=jms&loanProviders=ws&loanProviders=local&loanProcessors=funds&loanProcessors=down&loanProcessors=combined&message=jms.shutdown.success")
    assert shutdown.status_code == 200
    logging.info("Shutdown is performed")
    clean = requests.post(f"{base_url}/db.htm",data={"action":"CLEAN"})
    assert clean.status_code == 200
    logging.info("Clean is performed")
    jms_startup = requests.post(f"{base_url}/jms.htm", data={"shutdown": "false"})
    assert jms_startup.status_code == 200
    logging.info("Request for JMS to startup is performed")
    startup = requests.get(
        f"{admin_url}?isJmsRunning=false&loanProviders=jms&loanProviders=ws&loanProviders=local&loanProcessors=funds&loanProcessors=down&loanProcessors=combined&message=jms.startup.success")
    assert startup.status_code == 200
    logging.info("Startup is performed")
    init = requests.post(f"{base_url}/db.htm", data={"action": "INIT"})
    assert init.status_code == 200
    logging.info("Init is performed")



