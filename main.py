import smtplib
import pandas as pd
import datetime as dt
import random as r
import os
from dotenv import load_dotenv

load_dotenv("credentials.env")  # Load your credentials file

my_email = os.getenv("MY_EMAIL")
my_password = os.getenv("MY_APP_PASSWORD") # Password extra-made for third programmes

def birthdays_dict():
    """See if today is the birthday of any person contained in "birthdays.csv. Returns a dictionary
     with names and email addresses"""
    now = dt.datetime.now()
    day_now = now.day
    month_now = now.month
    dict_names_emails = {}

    df = pd.read_csv('birthdays.csv')
    for index, row in df.iterrows():
        if row['month'] == month_now and row['day'] == day_now:
            dict_names_emails[f"entry_{index}"] = {"name": row['name'], "email": row['email']}
    return dict_names_emails



def substitute_letter(personal_data):
    """Chooses one template randomly and personalize the name. Returns the letter text"""
    letter_type = "letter_" + str(r.randint(1,3)) + ".txt"
    with open(f"letter_templates/{letter_type}", "r") as file:
        letter= file.readlines()
        letter_header_adapted = letter[0].replace("[NAME]", personal_data["name"])
        letter[0] = letter_header_adapted
        full_text = ''.join(letter)
    return full_text



def sending_emails():
    """Sends an email to all the people contained in the dictionary coming from the function birthdays_dict
     and with the content of the function substitute_letter"""
    dict_1 = birthdays_dict()
    for entry in dict_1.values():
        try:
            with smtplib.SMTP("smtp.gmail.com", 587) as connection:
                connection.starttls()
                connection.login(user=my_email, password=my_password)
                connection.sendmail(
                    from_addr=my_email,
                    to_addrs=entry["email"],
                    msg=f"Subject:Happy birthday!\n\n{substitute_letter(entry)}"
                )
            print(f"Email sent to {entry['name']} at {entry['email']}")
        except Exception as e:
            print(f"Failed to send email to {entry['name']} at {entry['email']}: {e}")

sending_emails()




