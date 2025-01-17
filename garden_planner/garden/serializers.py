from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Plant, Garden, GardenPlant, WateringSchedule


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id","email", "username", "password"]
        extra_kwargs = {"password": {"write_only": True},  
                        "email":{"required": True},}

    def validate_email(self, value):
        if not value:  # Check for empty string or None
            raise serializers.ValidationError("Email is required.")
        return value


    def create(self, validated_data):
        print(validated_data)
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


    class Meta:
        model = GardenPlant
        #fields = ['id', 'plant', 'garden', 'quantity', 'planting_date', 'notes']
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

