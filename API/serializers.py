from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Prediction

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        min_length=6
    )

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)   #This hashes the password
        user.save()
        return user
    

class PredictionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Prediction
        fields = [
            'id',
            'user',
            'uploaded_image',
            'predicted_label',
            'confidence_score',
            'created_at'
        ]
        read_only_fields = [
            'user',
            'predicted_label',
            'confidence_score',
            'created_at'
        ]

class PredictionResultSerializer(serializers.ModelSerializer):

    class Meta:
        model = Prediction
        fields = [
            'id',
            'uploaded_image',
            'predicted_label',
            'confidence_score',
            'created_at'
        ]