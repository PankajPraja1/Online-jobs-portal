from rest_framework import serializers
from .models import User, Profile, Job, Application
from django.contrib.auth import get_user_model

UserModel = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ("id","username","email","is_employer","first_name","last_name")

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    class Meta:
        model = UserModel
        fields = ("username","email","password","is_employer","first_name","last_name")
    def create(self, validated_data):
        user = UserModel.objects.create_user(
            username=validated_data["username"],
            email=validated_data.get("email",""),
            password=validated_data["password"],
            is_employer=validated_data.get("is_employer", False),
            first_name=validated_data.get("first_name",""),
            last_name=validated_data.get("last_name",""),
        )
        return user

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ("headline","location")

class JobSerializer(serializers.ModelSerializer):
    employer = UserSerializer(read_only=True)
    class Meta:
        model = Job
        fields = ("id","employer","title","description","location","min_experience","skills","created_at")

class JobCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = ("title","description","location","min_experience","skills")

class ApplicationSerializer(serializers.ModelSerializer):
    candidate = UserSerializer(read_only=True)
    job = JobSerializer(read_only=True)
    class Meta:
        model = Application
        fields = ("id","job","candidate","resume","cover_letter","score","created_at")
