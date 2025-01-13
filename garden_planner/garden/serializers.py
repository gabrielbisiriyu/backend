from django.contrib.auth.models import User
from rest_framework import serializers



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


