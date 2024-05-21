from rest_framework import serializers
from .models import UAV, User, Rent, Model, Brand,Category

class UAVSerializer(serializers.ModelSerializer):
    class Meta:
        model = UAV
        fields = ["id","description", "weight", "model", "category", "image", "hourly_price", "is_active", "created_at", "owner"]

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "first_name", "last_name", "email", "password","username"]
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
    
class RentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rent
        fields = "__all__"

class ModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Model
        fields = "__all__"

class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = "__all__"

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"
