from django.contrib import admin
from django.urls import path, include
from garden.views import CreateUserView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.contrib.auth import views as auth_views 
from garden.views import PlantViewSet, GardenViewSet, GardenPlantViewSet, WateringScheduleViewSet,NotificationsAPIView, LogoutView,UserProfileView
from rest_framework.routers import DefaultRouter  
from django.conf import settings
from django.conf.urls.static import static




router = DefaultRouter()
router.register(r'plants', PlantViewSet, basename='plant')  # Register PlantViewSet for handling plants
router.register(r'garden', GardenViewSet, basename='garden')  # Register GardenViewSet for handling gardens
router.register(r'garden-plants', GardenPlantViewSet, basename='garden-plant')  # Register GardenPlantViewSet for garden-plant relationships
router.register(r'watering-schedules', WateringScheduleViewSet, basename='watering-schedule') #use the url/pk/ to update the water schedule form
#router.register(r'maintenance-tasks', MaintenanceTaskViewSet)



urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/register/", CreateUserView.as_view(), name="register"),
    path("api/token/", TokenObtainPairView.as_view(), name="get_token"),
    #path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="refresh"),
    path("api-auth/", include("rest_framework.urls")),
    path("api/profile/", UserProfileView.as_view(), name="user-profile"),    
    path("api/logout/", LogoutView.as_view(), name="logout"),
    path("api/notifications/", NotificationsAPIView.as_view(), name="notifications"),
    #path("api/garden-plants/<int:garden_plant_id>/complete-maintenance/", MaintenanceTaskCompletionView.as_view(), name="complete_maintenance"),
    path('api/', include(router.urls)),  # API endpoints for plants, gardens, and garden-plant relationships
    

]   + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
