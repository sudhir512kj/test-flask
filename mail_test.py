from flask_mail import Mail, Message
from flask import Flask
 
app = Flask(__name__)
mail = Mail(app)
 
@app.route("/mail")
def email():
    msg = Message("Hello Message", sender="admin@test.com", recipients=["to@test.com"])
    mail.send(msg)
    return {}