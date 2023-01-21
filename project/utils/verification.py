from flask import render_template, current_app
from flask import url_for, render_template
from itsdangerous import URLSafeTimedSerializer
from flask_mail import Mail, Message

mail = Mail()


def generate_confirmation_token(email):
    serializer = URLSafeTimedSerializer('SECRET_KEY')
    return serializer.dumps(email, salt='SECURITY_PASSWORD_SALT')


def confirm_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer('SECRET_KEY')
    try:
        email = serializer.loads(
            token,
            salt='SECURITY_PASSWORD_SALT',
            max_age=expiration
        )
    except:
        return False
    return email

def send_verification_email(user_email):
    token = generate_confirmation_token(user_email)
    confirm_url = url_for('auth.confirm_email', token=token, _external=True)
    html = render_template('verify_email.html', confirm_url=confirm_url)
    subject = "Please confirm your email"
    send_email(user_email, subject, html)

def send_email(to, subject, template):
    mail.init_app(current_app)
    msg = Message(subject, recipients=[to], html=template, sender=current_app.config['MAIL_USERNAME'])
    mail.send(msg)
    print("sent email to "+str(to))