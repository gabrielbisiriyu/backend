from django.db import models
from django.contrib.auth.models import User

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
    #notes = models.TextField(blank=True)

    class Meta:
        unique_together = ('garden', 'plant')

    def __str__(self):
        return f"{self.plant.name} in {self.garden.name}"