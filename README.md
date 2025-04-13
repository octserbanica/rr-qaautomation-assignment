# QA Automation Assignment

This project contains automated tests for the Parabank demo application (https://parabank.parasoft.com/parabank/index.htm), covering both API and UI functionalities.

## Technologies Used
- Python + Pytest
- Requests (API)
- Selenium (UI)
- Pytest-HTML for reports
- Logging for debugging

## 🚀 How to run tests

Install dependencies:
```
pip install -r requirements.txt
```

Run all tests:
```
Execute run_tests.bat from the root folder of the project 
```

Run only API tests:
```
pytest tests/test_api_parabank.py
```

Run only UI tests:
```
pytest tests/test_ui_parabank.py
```
