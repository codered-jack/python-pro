import requests

SHEETY_ENDPOINT = "https://api.sheety.co/******************"
SHEETY_API = "**********************************"
headers = {"apikey": SHEETY_API}

def get_customer_email():
    """Return customer rows from Sheety.

    Example return:
    [{"firstName": "John", "lastName": "Doe", "email": "john@example.com"}]
    """
    customer_data = requests.get(SHEETY_ENDPOINT)

    customer_data.raise_for_status()
    customer_information = customer_data.json()['users']

    return customer_information


def add_customer(first_name, last_name, email):
    """Insert one customer in Sheety.

    Example payload:
    {
        "user": {
            "firstName": "John",
            "lastName": "Doe",
            "email": "john@example.com"
        }
    }
    """
    user_information = {
        "user": {
            "firstName": first_name,
            "lastName": last_name,
            "email": email,
        }
    }
    response = requests.post(url=SHEETY_ENDPOINT, json=user_information, headers=headers)
    response.raise_for_status()
    return response


def prompt_and_register_customer():
    """CLI flow to register one customer interactively."""
    print("Welcome to Mik's Flight Club! \nWe find the best flight deals and email you.")
    first_name = input("What is your first name?: ").capitalize()
    last_name = input("What is your last name?: ").capitalize()
    email1 = input("What is your email? ")
    email2 = input("Type your email again. ")

    if email1 != email2:
        print("Your emails don't match. Please try again.")
        return

    add_customer(first_name, last_name, email1)
    print(
        f"Success! Thank you {first_name} {last_name}. "
        f"Your email {email1} has been added, you're in the club!"
    )


if __name__ == "__main__":
    prompt_and_register_customer()