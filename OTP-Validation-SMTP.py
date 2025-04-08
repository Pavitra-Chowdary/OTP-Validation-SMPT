import smtplib
import random
import os
import re
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Generate OTP
otp = random.randint(1111, 9999)
body = f"OTP for Verification is {otp}\nThis OTP is valid for 2 minutes."

def is_valid_email(email):
    """Validate email format"""
    return re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", email)

# Get recipient email
email_to = input("Enter Email ID: ")
while not is_valid_email(email_to):
    print("Invalid email format. Please try again.")
    email_to = input("Enter Email ID: ")

msg = MIMEMultipart()
msg["From"] = os.getenv("EMAIL_SENDER", "pavitrapavi1929@gmail.com")
msg["To"] = email_to
msg["Subject"] = "OTP For Validation"
msg.attach(MIMEText(body, 'plain'))

try:
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    sender_email = os.getenv("EMAIL_SENDER", "pavitrachowdary29@gmail.com")
    sender_password = os.getenv("EMAIL_PASSWORD", "eawe hjbu zdrq ysns")
    server.login(sender_email, sender_password)
    server.send_message(msg)
    server.quit()
    print("OTP Sent Successfully!")
except Exception as e:
    print(f"Failed to send OTP: {e}")
    exit()

# OTP Verification with retry mechanism
time_limit = time.time() + 120  # 2-minute timeout
attempts = 3
while attempts > 0:
    try:
        cotp = int(input("Enter OTP Received: "))
        if time.time() > time_limit:
            print("OTP has expired. Request a new one.")
            break
        if otp == cotp:
            print("OTP Verification Successful!")
            break
        else:
            attempts -= 1
            print(f"Invalid OTP. {attempts} attempts left.")
    except ValueError:
        print("Please enter a valid numeric OTP.")
        attempts -= 1
    
if attempts == 0:
    print("Too many incorrect attempts. Try again later.")
