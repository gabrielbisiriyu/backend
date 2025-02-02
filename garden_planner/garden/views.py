from django.shortcuts import render
from django.contrib.auth.models import User 
from .models import Plant, Garden, GardenPlant, WateringSchedule, Notification
from rest_framework import generics, viewsets
from .serializers import UserSerializer, PlantSerializer, GardenPlantSerializer, GardenSerializer, WateringScheduleSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny 
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404 
from datetime import date 
from rest_framework.filters import SearchFilter
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.exceptions import ValidationError
# Create your views here.


class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]   





class LogoutView(APIView):
    """
    Logout View for Blacklisting the Refresh Token.
    """
    def post(self, request):
        try:
            # Get the refresh token from the request data
            refresh_token = request.data.get("refresh_token")
            if refresh_token:
                token = RefreshToken(refresh_token)
                #return Response({"message": "Token is valid and ready for blacklisting"}, status=status.HTTP_200_OK)
                token.blacklist()  # Blacklist the token (requires blacklist app installed)
            return Response({"message": "Logout successful"}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)


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
        # Check if the plant already exists in the garden
        if GardenPlant.objects.filter(garden=garden, plant=plant).exists():
            raise ValidationError(f"The plant '{plant.name}' is already in the garden '{garden.name}'.")
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
    
    @action(detail=True, methods=['post'], url_path='mark-watered')
    def mark_watered(self, request, pk=None):
        schedule = self.get_object()
        schedule.last_watered_date = date.today()
        schedule.save()

        return Response({"message": f"{schedule.garden_plant.plant.name} has been watered."})   

 

class NotificationsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Fetch notifications for the logged-in user. 
        Optionally, fetch a specific notification by ID.
        """
        notification_id = request.query_params.get("id")
        if notification_id:
            # Fetch a specific notification
            notification = request.user.notifications.filter(id=notification_id).first()
            if notification:
                data = {
                    "id": notification.id,
                    "message": notification.message,
                    "is_read": notification.is_read,
                    "created_at": notification.created_at,
                }
                return Response(data)
            return Response({"error": "Notification not found."}, status=404)
        
        # Fetch all unread notifications if no ID is provided
        notifications = request.user.notifications.filter(is_read=False)
        data = [
            {
                "id": n.id,
                "message": n.message,
                "is_read": n.is_read,
                "created_at": n.created_at,
            }
            for n in notifications
        ]
        return Response(data)


