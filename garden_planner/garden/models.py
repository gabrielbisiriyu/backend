from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta, date, timezone, datetime
from cloudinary.models import CloudinaryField
# Create your models here.

class Plant(models.Model):
    name = models.CharField(max_length=200)
    plant_type = models.CharField(max_length=100)
    #image = models.ImageField(upload_to='plant_image/', null=True, blank=True)
    #image = models.ImageField(upload_to='images',null=True,blank=True) # image    
    image = CloudinaryField("image",blank=True,null=True)
    SUNLIGHT_CHOICES = [
        ('LOW', 'Low Light'),
        ('MEDIUM', 'Medium Light'),
        ('HIGH', 'Bright Light')
    ]
    sunlight = models.CharField(max_length=50, choices=SUNLIGHT_CHOICES)
    soil = models.CharField(max_length=500)
    water_frequency = models.IntegerField(help_text="Number of days per week")
    maintenance_task = models.TextField(blank=True, help_text="Maintenance tasks for the plant (e.g., pruning, fertilizing).")
    number_of_days_to_Harvest = models.IntegerField(null=True, blank=True, help_text="Expected days harvest")

    
    def __str__(self):
        return self.name  
    

class Garden(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name="gardens") 
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class GardenPlant(models.Model):
    garden = models.ForeignKey(Garden, on_delete=models.CASCADE)
    plant = models.ForeignKey(Plant, on_delete=models.CASCADE)  # Assuming Plant is in a separate app named 'plants'
    quantity = models.IntegerField(default=1)
    planting_date = models.DateField(null=True, blank=True)
    harvest_due_date = models.DateField(null=True, blank=True)  # Auto-calculated based on planting_date and number_of_days_to_Harvest
    growth_stage = models.CharField(max_length=50, choices=[('SEEDLING', 'Seedling'), ('VEGETATIVE', 'Vegetative'), ('FLOWERING', 'Flowering'), ('FRUITING', 'Fruiting')], blank=True, null=True)

    class Meta:
        unique_together = ('garden', 'plant')

    def save(self, *args, **kwargs):
        # Call the original save method
        # Automatically calculate harvest_due_date
        if self.planting_date and self.plant.number_of_days_to_Harvest:
            self.harvest_due_date = self.planting_date + timedelta(days=self.plant.number_of_days_to_Harvest)   

        # Optionally set growth_stage based on plant age (assuming average growth timeline)
        if self.planting_date:
            days_since_planting = (date.today() - self.planting_date).days
            if days_since_planting <= (self.plant.number_of_days_to_Harvest)*0.15:
                self.growth_stage = 'SEEDLING'
            elif days_since_planting <= (self.plant.number_of_days_to_Harvest)*0.45:
                self.growth_stage = 'VEGETATIVE'
            elif days_since_planting <= (self.plant.number_of_days_to_Harvest)*0.78:
                self.growth_stage = 'FLOWERING'
            else:
                self.growth_stage = 'FRUITING'   
        super().save(*args, **kwargs)


            #super().save(*args, **kwargs)

        # Check if a watering schedule already exists for this garden plant
        if not WateringSchedule.objects.filter(garden_plant=self).exists():
            # Automatically create a WateringSchedule using the plant's default watering frequency
            WateringSchedule.objects.create(
                garden_plant=self,
                frequency_in_days=self.plant.water_frequency,
                next_watering_date=(self.planting_date or date.today()) + timedelta(days=self.plant.water_frequency)
            )

    def __str__(self):
        return f"{self.plant.name} in {self.garden.name}"  
    



class WateringSchedule(models.Model):
    garden_plant = models.ForeignKey(GardenPlant, on_delete=models.CASCADE, related_name='watering_schedules')
    next_watering_date = models.DateField()
    frequency_in_days = models.IntegerField(default=7)  # Default frequency of 7 days
    last_watered_date = models.DateField(null=True, blank=True)

    def save(self, *args, **kwargs):
        # Automatically calculate the next watering date if last watered
        if self.last_watered_date:
            self.next_watering_date = self.last_watered_date + timedelta(days=self.frequency_in_days)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Watering Schedule for {self.garden_plant.plant.name} in {self.garden_plant.garden.name}"
        


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    #task_type = models.CharField(max_length=20, choices=[('WATERING', 'Watering'), ('MAINTENANCE', 'Maintenance')], blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user.username}"
    


