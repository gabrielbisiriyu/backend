from django.contrib import admin
from django.urls import path, include
from garden.views import CreateUserView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.contrib.auth import views as auth_views 
from garden.views import PlantViewSet, GardenViewSet, GardenPlantViewSet
from rest_framework.routers import DefaultRouter  



router = DefaultRouter()
router.register(r'plants', PlantViewSet, basename='plant')  # Register PlantViewSet for handling plants
router.register(r'garden', GardenViewSet, basename='garden')  # Register GardenViewSet for handling gardens
router.register(r'garden-plants', GardenPlantViewSet, basename='garden-plant')  # Register GardenPlantViewSet for garden-plant relationships




urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/register/", CreateUserView.as_view(), name="register"),
    path("api/token/", TokenObtainPairView.as_view(), name="get_token"),
    #path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("api/tokenrefresh", TokenRefreshView.as_view(), name="refresh"),
    path("api-auth/", include("rest_framework.urls")),
    path('api/', include(router.urls)),  # API endpoints for plants, gardens, and garden-plant relationships
    

]     
