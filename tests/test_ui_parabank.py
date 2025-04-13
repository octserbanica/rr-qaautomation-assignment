import time
import random
import json
import re
from selenium.webdriver.common.by import By
import logging
import pytest

@pytest.mark.run(order =1)
def test_ui_register_user(base_url, user_data, driver):

    driver.get(base_url + "/register.htm")
    time.sleep(2)

    rand = random.randint(1000, 9999)
    username = f"octavian_ui_{rand}"
    password = "TestPass123"

    driver.find_element(By.NAME, "customer.firstName").send_keys("Octavian")
    driver.find_element(By.NAME, "customer.lastName").send_keys("Tester")
    driver.find_element(By.NAME, "customer.address.street").send_keys("Sesame")
    driver.find_element(By.NAME, "customer.address.city").send_keys("Craiova")
    driver.find_element(By.NAME, "customer.address.state").send_keys("Dolj")
    driver.find_element(By.NAME, "customer.address.zipCode").send_keys("200000")
    driver.find_element(By.NAME, "customer.phoneNumber").send_keys("0722000000")
    driver.find_element(By.NAME, "customer.ssn").send_keys("123-45-6789")
    driver.find_element(By.NAME, "customer.username").send_keys(username)
    driver.find_element(By.NAME, "customer.password").send_keys(password)
    driver.find_element(By.NAME, "repeatedPassword").send_keys(password)

    driver.find_element(By.CSS_SELECTOR, "input.button[value='Register']").click()
    time.sleep(2)

    success_message = driver.find_element(By.CLASS_NAME, "title").text
    assert "Welcome" in success_message or "successfully" in driver.page_source, "The user was not registered"
    logging.info("Registration is valid")

    driver.find_element(By.LINK_TEXT, "Accounts Overview").click()

    customer_id = None
    for request in driver.requests:
        if request.response and "services_proxy/bank/customers" in request.url:
            match = re.search(r'/customers/(\d+)/accounts', request.url)
            if match:
                customer_id = match.group(1)
                break

    if not customer_id:
        raise Exception("Customer ID not found in captured requests")

    user_data = {
        "username": username,
        "password": password,
        "customer_id": customer_id
    }

    with open("user_data.json", "w") as f:
        json.dump(user_data, f)

    logging.info(f"The user '{username}' was registered and saved in user_data.json!")

