from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta

# Create your models here.

class Plant(models.Model):
    name = models.CharField(max_length=200)
    plant_type = models.CharField(max_length=100)
    image = models.ImageField(upload_to='plant_image/', null=True, blank=True)
    
    # Growing requirements
    SUNLIGHT_CHOICES = [
        ('LOW', 'Low Light'),
        ('MEDIUM', 'Medium Light'),
        ('HIGH', 'Bright Light')
    ]
    sunlight = models.CharField(max_length=50, choices=SUNLIGHT_CHOICES)
    soil = models.CharField(max_length=500)
    water_frequency = models.IntegerField(help_text="Number of days per week")
    # Care instructions  
    fertilizer_instructions = models.TextField()
    pruning_instructions = models.TextField()
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
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

    class Meta:
        unique_together = ('garden', 'plant')

    def save(self, *args, **kwargs):
        # Call the original save method
        super().save(*args, **kwargs)

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
        