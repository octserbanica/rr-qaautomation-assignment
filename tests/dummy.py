import requests

# Cream o sesiune
session = requests.Session()

# Header explicit
headers = {
    "Content-Type": "application/x-www-form-urlencoded"
}

# Endpoint login
url = "https://parabank.parasoft.com/parabank/login.htm"

# Date login (vechiul username mergea: john / demo)
payload = {
    "username": "octavian1",
    "password": "parola123"
}

# Trimitere request
response = session.post(url, data=payload, headers=headers)

# Debug: status, redirect, cookies, body
print("Status code:", response.status_code)
print("Redirected to:", response.url)
print("Cookies:", session.cookies.get_dict())
print("Snippet din response:")
print(response.text[:500])  # doar începutul paginii pentru context
