import os
from celery import Celery
from django.conf import settings
import logging
from django.utils import timezone
from django.apps import apps
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from decouple import config
import time
from celery.schedules import crontab

logger = logging.getLogger(__name__)

# Set the Django settings module for Celery
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "passportBackend.settings")

# Create a Celery instance
app = Celery("tasks", broker="pyamqp://guest@localhost//")

# Load task modules from all registered Django app configs.
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

#
# 0.-- sudo mkdir /var/run/celery
# 0.-- sudo chown vagrant:vagrant /var/run/celery
#
# Service file: celery.service ---- Celery ----
#
# 1. sudo systemctl daemon-reload
# 2. sudo systemctl enable celery
# 3. sudo systemctl restart celery
# 4. sudo systemctl status celery.service

#
# Service file: celerybeat.service --- Celery Beat: --
#
# 1. sudo systemctl daemon-reload
# 2. sudo systemctl enable celerybeat.service
# 3. sudo systemctl start celerybeat.service
# 4. sudo systemctl status celerybeat.service
#

# For test
#
# celery -A polls.scheduleTasksPassport.t1_ExpiryNotification worker -l INFO
# python manage.py shell


#
# Tests
#
# @app.on_after_configure.connect
# def setup_periodic_tasks(sender, **kwargs):

#     Calls test('hello') #every 10 seconds.
#     sender.add_periodic_task(10.0, test.s("hello22"), name="add every 10")

#     Calls test('hello') #every 10 seconds.
#     sender.add_periodic_task(100.0, sendExpiryNotification.s(), name="add every 10")


# -----
#
# Passport Expiration Reminder
#
# Runs every day at midnight
#
app.conf.beat_schedule = {
    # Executes at sunset in Melbourne
    "add-at-melbourne-sunset": {
        "task": "t1_ExpiryNotification.sendExpiryNotification",
        "schedule": crontab(minute=0, hour=0),  # Execute daily at midnight.
    },
}


#
# Passport Expiration Reminder
#
@app.task
def sendExpiryNotification():

    #
    # Subject
    #
    subject = "Passport Expiration Reminder"

    #
    # From Email
    #
    from_email = config("EMAIL_HOST_USER")

    #
    # Template path
    #
    BASE_DIR = settings.BASE_DIR
    template_path = os.path.join(
        BASE_DIR,
        "polls",
        "templates",
        "emailTemplates",
        "expiryPassportNotification.html",
    )
    #
    # Passport Model
    #
    # Get the passports for users who have not received notification
    #
    # For 1 month prior
    #
    model = apps.get_model(app_label="polls", model_name="Passport")
    one_month_from_now = timezone.now() + timezone.timedelta(days=30)
    passports = model.objects.filter(
        date_of_expiry=one_month_from_now, email_updated_expiry=False
    )

    for passport in passports:

        context = {
            "first_name": passport.user.first_name,
            "last_name": passport.user.last_name,
        }
        html_content = render_to_string(template_path, context)
        text_content = strip_tags(html_content)

        to_email = passport.user.email

        email = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
        email.attach_alternative(html_content, "text/html")

        #
        # Add a 15-second delay for sent email
        #
        time.sleep(15)

        email.send()

        passport.email_updated_expiry = True
        passport.save()

        # print("Sending email to ", to_email)


#
# TEST SCHEDULE TASK
#
# @app.task
# def test(arg):
#     logger.info("KU JE RE")
#     subject = "Your Subject Here"
#     message = "Your Message Here"
#     from_email = "it21964@hua.gr"
#     recipient_list = ["arisdulla7@gmail.com"]
#     logger.info("Sending email to arisdulla7@gmail.com")
#     send_mail(subject, message, from_email, recipient_list)
#     logger.info(arg)
