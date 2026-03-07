from datetime import datetime as dt
import pandas
import random
import smtplib


my_email = "myemail@email.com"
password = "your_password"

#Get the current date
now = dt.now()
today = (now.month, now.day)

#Read CSV
birthdays = pandas.read_csv("birthdays.csv")

birthdays_dict = {(row.month, row.day): row for (index, row) in birthdays.iterrows()}
# print(birthdays_dict)


if today in birthdays_dict:
    letter_to_send = f"./letter_templates/letter_{random.randint(1,3)}.txt"
    with open(letter_to_send) as birthday_card:
        birthday_person = birthdays_dict[today]
        letter_contents = birthday_card.read()
        new_letter = letter_contents.replace("[NAME]", birthday_person["name"])

    with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
        connection.starttls()
        connection.login(user=my_email, password=password)
        connection.sendmail(from_addr=my_email, to_addrs=birthday_person["email"],
                            msg=f"Subject:Happy Birthday\n\n{new_letter}\n")