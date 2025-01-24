from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Plant, Garden, GardenPlant, WateringSchedule
from datetime import date 


from django.contrib.auth.models import User
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True, required=True)  # Add confirm_password as a write-only field

    class Meta:
        model = User
        fields = ["id", "email", "username", "password", "confirm_password"]
        extra_kwargs = {
            "password": {"write_only": True},
            "email": {"required": True},
        }

    def validate_email(self, value):
        if not value:  # Check for empty string or None
            raise serializers.ValidationError("Email is required.")
        return value

    def validate(self, data):
        # Check if password and confirm_password match
        if data["password"] != data["confirm_password"]:
            raise serializers.ValidationError({"confirm_password": "Passwords do not match."})
        return data

    def create(self, validated_data):
        # Remove confirm_password from validated_data since it's not a model field
        validated_data.pop("confirm_password")
        user = User.objects.create_user(**validated_data)
        return user



class PlantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plant
        #fields = '__all__' 
        fields =  ['id', 'name', "plant_type","image", "sunlight", "soil","water_frequency","fertilizer_instructions","pruning_instructions"  ]        


class GardenSerializer(serializers.ModelSerializer):

    class Meta:
        model = Garden
        fields =  ['id', 'name']


class GardenPlantSerializer(serializers.ModelSerializer):
    #plant = PlantSerializer()
    #garden = GardenSerializer()
    garden = serializers.PrimaryKeyRelatedField(queryset=Garden.objects.all())
    plant = serializers.PrimaryKeyRelatedField(queryset=Plant.objects.all()) 
    watering_schedule = serializers.SerializerMethodField()

    # Auto-generate `quantity` (default to 1)
    quantity = serializers.IntegerField(required=False, default=1)

    # Auto-fill `planting_date` with today's date
    planting_date = serializers.DateField(required=False, default=date.today)

    class Meta:
        model = GardenPlant
        #fields = ['id', 'plant', 'garden', 'quantity', 'planting_date']
        fields = ['id', 'plant', 'garden', 'quantity', 'planting_date', 'watering_schedule']

    def get_watering_schedule(self, obj):
        schedule = WateringSchedule.objects.filter(garden_plant=obj).first()
        if schedule:
            return {
                'next_watering_date': schedule.next_watering_date,
                'frequency_in_days': schedule.frequency_in_days,
                'last_watered_date': schedule.last_watered_date,
            }
        return None

    def create(self, validated_data):
        garden_plant = super().create(validated_data)
        return garden_plant


class WateringScheduleSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = WateringSchedule
        fields = ['id', 'garden_plant', 'frequency_in_days', 'next_watering_date', 'last_watered_date'] 

