import pytest
import requests
import json
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'helpers')))
from selenium.webdriver.chrome.options import Options
from seleniumwire import webdriver



@pytest.fixture
def user_data():
    try:
        with open("user_data.json", "r") as f:
            user_data = json.load(f)
    except FileNotFoundError:
        user_data = None
    return user_data


@pytest.fixture
def driver():
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--window-size=1920,1080")
    driver = webdriver.Chrome(options=options)
    yield driver
    driver.quit()

@pytest.fixture(scope="session")
def base_url():
    return "https://parabank.parasoft.com/parabank"

@pytest.fixture(scope="session")
def authenticated_session(base_url, user_data):
    with open("user_data.json", "r") as f:
        user_data = json.load(f)

    username = user_data["username"]
    password = user_data["password"]

    session = requests.Session()
    login_url = f"{base_url}/login.htm"
    payload = {"username": username, "password": password}
    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    response = session.post(login_url, data=payload, headers=headers)
    assert response.status_code == 200, "Login failed"
    assert "Accounts Overview" in response.text or "Welcome" in response.text

    session.base_url = base_url  # Salvăm base_url în sesiune

    return session

@pytest.fixture(params=[
    (1000, 100),
    (5000, 500),
    (15000, 2000),
    (100, 10),
    (3000, 0),
])
def loan_data(request):
    return request.param