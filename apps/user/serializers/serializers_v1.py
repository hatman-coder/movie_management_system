from ..models import User
from rest_framework import serializers


excluded_list = ["is_active", "created_at", "updated_at"]


class UserListSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField(read_only=True)

    @staticmethod
    def get_name(obj):
        return str(obj.get_full_name())

    class Meta:
        model = User
        exclude = excluded_list + [
            "password",
            "last_login",
            "is_staff",
            "is_superuser",
            "groups",
            "user_permissions",
            "first_name",
            "last_name",
        ]


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=128, allow_blank=False, allow_null=False
    )

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "email",
            "username",
            "password",
            "role",
            "phone_number",
        ]


class AdminCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=128, allow_blank=False, allow_null=False
    )

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "email",
            "username",
            "password",
            "role",
            "phone_number",
            "is_superuser",
            "is_staff",
        ]


class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = excluded_list + [
            "password",
            "last_login",
            "is_staff",
            "is_superuser",
            "groups",
            "user_permissions",
            "role",
        ]


class UpdateProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = excluded_list + [
            "password",
            "last_login",
            "is_staff",
            "is_superuser",
            "groups",
            "user_permissions",
            "role",
        ]
