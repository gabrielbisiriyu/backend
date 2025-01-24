from celery import shared_task, Task
from django.core.mail import send_mail
from django.utils.timezone import now
from .models import WateringSchedule, Notification
from time import sleep



#@shared_task
def send_watering_reminders():
    today = now().date()
    print("hellllllllo")  # Add this line
    schedules_due = WateringSchedule.objects.filter(next_watering_date=today)
    print(f"Schedules due: {schedules_due}")  # Debugging log
    for schedule in schedules_due:
        user_email = schedule.garden_plant.garden.user.email
        plant_name = schedule.garden_plant.plant.name
        garden_name = schedule.garden_plant.garden.name

        # Send email
        send_mail(
            subject="Watering Reminder",
            message=f"Reminder: It's time to water {plant_name} in your garden {garden_name}.",
            from_email="no-reply@gardenapp.com",
            recipient_list=[user_email],
        
        )  



#@shared_task
