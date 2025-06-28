from django.core.mail import send_mail
from django.conf import settings
def send_account_activation_email(email_token, email):
    subject = 'Ýour account needs to be activated'
    message = f'Hi, click on the link to activated your account http://127.0.0.1:8000/account/activated/{email_token}'
    from_email = settings.EMAIL_HOST_USER
    send_mail(
        subject, 
        message, 
        from_email, 
        [email]
        #recipient_list
    )