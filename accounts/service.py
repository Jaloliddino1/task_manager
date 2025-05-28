from django.core.mail import send_mail
from django.conf import settings

def send_email(subject, message, to_email):
        send_mail(subject=subject,
                  message=message,
                  from_email='utkurovikromjon0@gmail.com',
                  recipient_list=[to_email],
                  fail_silently=True
                  )