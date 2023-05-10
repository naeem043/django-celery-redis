from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.core.mail import send_mail
from celery import shared_task
from celery_project import settings
from django.utils import timezone
from datetime import timedelta

@shared_task(bind=True)
def update_inactive_users(self):
    users = User.objects.all().exclude(id=1)
    #timezone.localtime(users.date_time) + timedelta(days=2)
    for user in users:
        print('update ====',user)
        User.objects.filter(id = user.id).update(is_staff=True, is_active=True)
    return "Task Done"

@shared_task(bind=True)
def send_mail_task(self):
    users = get_user_model().objects.all()
    #timezone.localtime(users.date_time) + timedelta(days=2)
    for user in users:
        try:
            mail_subject = "Hi! Celery Testing"
            message = "This is the testing mail from the celery & redis"
            to_email = user.email
            print('to_email====',to_email)
            send_mail(
                subject = mail_subject,
                message=message,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[to_email],
                fail_silently=True,
            )
        except Exception as e:
            print('Error::',str(e))
            
    return "Done"