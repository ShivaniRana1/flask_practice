# from flask import Flask
# import requests


# app = Flask(__name__)

# Configure Flask-Mail to use SendGrid SMTP
# app.config['MAIL_SERVER'] = 'smtp.mailersend.net'
# app.config['MAIL_PORT'] = 587
# app.config['MAIL_USE_TLS'] = True
# app.config['MAIL_USERNAME'] = 'MS_zbiPIh@trial-3vz9dle7wdn4kj50.mlsender.net'  # SendGrid API key as the username
# app.config['MAIL_PASSWORD'] = '587'  # SendGrid SMTP password





from mailersend import emails

api_key = "mlsn.57cb852bbfb6612edbfa37df8884937be307c4d8f5973447361724aec79b0b9c"

mailer = emails.NewEmail(api_key)

# define an empty dict to populate with mail values
mail_body = {}

mail_from = {
    "name": "Shivani Rana",
    "email": "ranapriya123456789@gmail.com",
}

recipients = [
    {
        "name": "Shivani Rana",
        "email": "ranashivani316@gmail.com",
    }
]

reply_to = [
    {
        "name": "Shivani Rana",
        "email": "ranashivani316@gmail.com",
    }
]

mailer.set_mail_from(mail_from, mail_body)
mailer.set_mail_to(recipients, mail_body)
mailer.set_subject("Hello!", mail_body)
mailer.set_html_content("This is the HTML content", mail_body)
mailer.set_plaintext_content("This is the text content", mail_body)
mailer.set_reply_to(reply_to, mail_body)

# using print() will also return status code and data
mailer.send(mail_body)
print(mail_body)