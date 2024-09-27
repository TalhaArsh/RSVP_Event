
from flask import Flask, render_template, request, redirect, url_for
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pymongo import MongoClient
import os
from dotenv import load_dotenv

app = Flask(__name__)

load_dotenv()

client = MongoClient(f"mongodb+srv://{os.getenv('MONGO_USERNAME')}:{os.getenv('MONGO_PASSWORD')}@cluster0.71tvv.mongodb.net/")
db = client['rsvp_db']
guests_collection = db['guests']


SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587


SENDER_EMAIL = os.getenv('EMAIL')
SENDER_PASSWORD = os.getenv('PASSWORDS')



def send_confirmation_email(to_email, name):
    subject = "RSVP Confirmation"
    body = f"Dear {name},\n\nThank you for RSVPing to our event! We look forward to seeing you there.\n\nBest Regards,\nTeenda Shelby"

    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = to_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))


    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, to_email, msg.as_string())
        server.quit()
        print("Email sent successfully!")
    except Exception as e:
        print(f"Error sending email: {e}")


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/rsvp', methods=['GET', 'POST'])
def rsvp():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']


        guests_collection.insert_one({'name': name, 'email': email})


        send_confirmation_email(email, name)

        return redirect(url_for('thank_you'))

    return render_template('rsvp.html')


@app.route('/thank-you')
def thank_you():
    return '<h2>Thank you for your RSVP!</h2>'


if __name__ == '__main__':
    app.run(debug=True)
