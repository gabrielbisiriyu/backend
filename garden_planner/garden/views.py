from django.shortcuts import render
from django.contrib.auth.models import User 
from .models import Plant, Garden, GardenPlant, WateringSchedule
from rest_framework import generics, viewsets
from .serializers import UserSerializer, PlantSerializer, GardenPlantSerializer, GardenSerializer, WateringScheduleSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny 
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404 
from datetime import date 
from rest_framework.filters import SearchFilter
# Create your views here.


class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]   



# View for managing available Plants (read-only for users)
class PlantViewSet(viewsets.ReadOnlyModelViewSet):  # Making it read-only as users cannot create plants
    queryset = Plant.objects.all()
    serializer_class = PlantSerializer
    permission_classes = [IsAuthenticated]  # Only authenticated users can access   
    filter_backends = [SearchFilter]  # Add search functionality
    search_fields = ['name']  # Specify fields to search (assuming 'name' is the plant name field)


# View for managing Gardens
class GardenViewSet(viewsets.ModelViewSet):
    queryset = Garden.objects.all()
    serializer_class = GardenSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)  # Automatically associate the garden with the logged-in user

    def get_queryset(self):
        return Garden.objects.filter(user=self.request.user)  # Users can only see their own gardens



# View for managing Garden-Plant relationships (adding/removing plants)
class GardenPlantViewSet(viewsets.ModelViewSet):
    queryset = GardenPlant.objects.all()
    serializer_class = GardenPlantSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Ensure users can only see plants in their own gardens
        return GardenPlant.objects.filter(garden__user=self.request.user)

    def perform_create(self, serializer):
        # Automatically associate the garden with the logged-in user
        garden = self.request.user.gardens.get(id=self.request.data['garden'])
        plant = get_object_or_404(Plant, id=self.request.data['plant'])  # Only valid plants can be added
        #serializer.save(garden=garden, plant=plant)
        # Automatically set planting_date to today's date
        serializer.save(garden=garden, plant=plant, planting_date=date.today())




class WateringScheduleViewSet(viewsets.ModelViewSet):
    queryset = WateringSchedule.objects.all()
    serializer_class = WateringScheduleSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Ensure users can only see watering schedules for their own garden plants
        return WateringSchedule.objects.filter(garden_plant__garden__user=self.request.user)  
    
