import sqlite3
import mysql.connector
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def connect_to_rds():
    try:
        conn = mysql.connector.connect(
            host="your-db.abc123xyz.us-east-1.rds.amazonaws.com",
            port=3306,
            user="your_username",
            password="your_password",
            database="database")
        status=200
        cursor=conn.cursor()
        return cursor,conn
    except:
        conn=sqlite3.connect("user.db")
        cursor=conn.cursor()
        return cursor,conn


def check_user(phone: str) -> str:
    cursor,conn=connect_to_rds()
    cursor.execute("SELECT name,phone,email,address_line_1,address_line_2,city,state,zipcode FROM users WHERE phone = ?", (phone,))
    row = cursor.fetchone()
    conn.close()
    if row:
        user_info={'Name':row[0],
                   'Phone':row[1],
                   'Email':row[2],
                   'Address':row[3]+" "+ (row[4] if row[4] is not None else ''),
                   "City": row[5],
                   "State":row[6],
                   "Zipcode":row[7]}
    if user_info:
        return f"User Exitst:{user_info}"
    else:
        return "User does not exist"

def new_user(name: str, phone_number:str,address:str,pincode:str,email_id:str,city:str,service_requested:str,datetime_of_appointment:str) -> str:
    return f"""User Details \n\n Name: {name}\n\n Phone Number: {phone_number}\n\n Address: {address}\n\n Pincode: {pincode}\n\n Email ID: {email_id}\n\n City: {city}\n\n Service Requested: {service_requested} \n\n date & time for service: {datetime_of_appointment}"""


def email_user(to_email:str):
    return (email_user)


def send_email(to_email, subject, message):
    from_email = "your_email@example.com"  # Replace with your email
    from_password = "your_password"  # Replace with your email password

    # Create a multipart message
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject

    msg.attach(MIMEText(message, 'plain'))

    try:
        with smtplib.SMTP('smtp.example.com', 587) as server:  # Replace with your SMTP server
            server.starttls()  # Upgrade to secure connection
            server.login(from_email, from_password)
            server.send_message(msg)
            print(f"Email sent to {to_email}")
    except Exception as e:
        print(f"Error sending email: {e}")
