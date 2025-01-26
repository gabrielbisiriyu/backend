from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.timezone import now
from .models import WateringSchedule, Notification,GardenPlant, Plant
from django.core.mail import send_mail
from datetime import timedelta, timezone
import threading
import logging   



def send_email_async(subject, message, from_email, recipient_list):
    def send():
        try:
            send_mail(
                subject,
                message,
                from_email,
                recipient_list,
                fail_silently=False
            )
        except Exception as e:
            logging.error(f"Email sending failed: {e}")
            
    
    threading.Thread(target=send, daemon=True).start()


@receiver(post_save, sender=WateringSchedule)
def create_notification_on_schedule_save(sender, instance, created, **kwargs):
    """
    Create an in-app notification when a watering schedule is due.
    """
    today = now().date()
    
    # Check if the schedule is due today
    if instance.next_watering_date == today:
        user = instance.garden_plant.garden.user
        plant_name = instance.garden_plant.plant.name
        garden_name = instance.garden_plant.garden.name
        message = f"Reminder: It's time to water {plant_name} in your garden {garden_name}."
        # Avoid duplicate notifications
        if not Notification.objects.filter(user=user, message=message, is_read=False).exists():
            Notification.objects.create(user=user, message=message)

    # Email Reminder
    if instance.next_watering_date == today:
        user_email = instance.garden_plant.garden.user.email
        plant_name = instance.garden_plant.plant.name
        garden_name = instance.garden_plant.garden.name

        send_email_async(
            subject="Watering Reminder",
            message=f"Reminder: It's time to water {plant_name} in your garden {garden_name}.",
            from_email="no-reply@gardenapp.com",
            recipient_list=[user_email],
        )





@receiver(post_save, sender=GardenPlant)
def create_harvest_and_maintenance_reminders(sender, instance, created, **kwargs):
    """
    Create notifications for harvest and maintenance tasks.
    """
    today = now().date()
    user = instance.garden.user
    plant_name = instance.plant.name

    # Harvest reminders: Start 7 days before the harvest_due_date
    if instance.harvest_due_date and today >= instance.harvest_due_date - timedelta(days=7):
        days_left = (instance.harvest_due_date - today).days
        if days_left >= 0:  # Notify daily until the harvest due date
            message = f"Reminder: {plant_name} is ready for harvest in {days_left} days (Harvest Date: {instance.harvest_due_date})."
            if not Notification.objects.filter(user=user, message=message, is_read=False).exists():
                Notification.objects.create(user=user, message=message)

    # Maintenance reminders: Weekly notifications
    if instance.plant.maintenance_task and today.weekday() == 0:  # Example: Monday reminders
        message = f"Reminder: {instance.plant.maintenance_task} is required for {plant_name} this week."
        if not Notification.objects.filter(user=user, message=message, is_read=False).exists():
            Notification.objects.create(user=user, message=message) 

    #Email reminder for havest due todat
    # Check if the harvest_due_date is today
    if instance.harvest_due_date and instance.harvest_due_date == today:
        user_email = instance.garden.user.email
        plant_name = instance.plant.name
        garden_name = instance.garden.name

        # Send email reminder
        send_email_async(
            subject="Harvest Reminder",
            message=f"Reminder: {plant_name} in your garden {garden_name} is ready for harvest today!",
            from_email="no-reply@gardenapp.com",
            recipient_list=[user_email],
        )
        


@receiver(post_save, sender=Plant)
def update_related_fields_on_plant_change(sender, instance, created, **kwargs):
    """
    Update related fields in GardenPlant and WateringSchedule models
    when the Plant's number_of_days_to_Harvest or water_frequency changes.
    """
    if not created:  # Only run this on updates
        # Update harvest_due_date in GardenPlant
        garden_plants = GardenPlant.objects.filter(plant=instance)
        for garden_plant in garden_plants:
            if garden_plant.planting_date and instance.number_of_days_to_Harvest:
                garden_plant.harvest_due_date = garden_plant.planting_date + timedelta(days=instance.number_of_days_to_Harvest)
                garden_plant.save()  # Save the updated harvest_due_date

        # Update frequency_in_days in WateringSchedule
        watering_schedules = WateringSchedule.objects.filter(garden_plant__plant=instance)
        for schedule in watering_schedules:
            schedule.frequency_in_days = instance.water_frequency
            # Recalculate the next_watering_date based on the new frequency
            if schedule.last_watered_date:
                schedule.next_watering_date = schedule.last_watered_date + timedelta(days=instance.water_frequency)
            else:
                # Use today as a fallback if last_watered_date is not set
                schedule.next_watering_date = schedule.garden_plant.planting_date + timedelta(days=instance.water_frequency)
            schedule.save()  # Save the updated watering schedule    






