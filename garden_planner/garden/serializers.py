from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Plant, Garden, GardenPlant


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
        fields = '__all__'


class GardenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Garden
        fields =  ['id', 'name']


class GardenPlantSerializer(serializers.ModelSerializer):
    #plant = PlantSerializer()
    #garden = GardenSerializer()
    garden = serializers.PrimaryKeyRelatedField(queryset=Garden.objects.all())
    plant = serializers.PrimaryKeyRelatedField(queryset=Plant.objects.all()) 



    class Meta:
        model = GardenPlant
        #fields = ['id', 'plant', 'garden', 'quantity', 'planting_date', 'notes']
        fields = ['id', 'plant', 'garden', 'quantity', 'planting_date']

