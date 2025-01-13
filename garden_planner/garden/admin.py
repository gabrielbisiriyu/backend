from django.contrib import admin
from .models import Plant, Garden, GardenPlant  # Import your Plant model

# Register your models here.
admin.site.register(Plant) 
admin.site.register(GardenPlant)
admin.site.register(Garden)