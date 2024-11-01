from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from ..serializers.serializers_v1 import *
from ..models import User
from external.enum import UserRole
from external.pagination import CustomPagination
from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from drf_spectacular.utils import extend_schema, OpenApiExample


class UserViewSet(viewsets.ModelViewSet):
    model_class = User
    permission_classes = [IsAuthenticated]
    serializer_class = UserListSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        return self.model_class.objects.all()

    def get_serializer_class(self):
        if self.action == "create_user":
            return UserCreateSerializer
        if self.action == "create_admin":
            return AdminCreateSerializer
        if self.action == "update_user":
            return UpdateUserSerializer
        if self.action == "update_my_profile":
            return UpdateProfileSerializer
        else:
            return self.serializer_class

    @extend_schema(
        tags=["User"],
        examples=[
            OpenApiExample(
                "Create User",
                value={
                    "first_name": "string",
                    "last_name": "string",
                    "email": "user@example.com",
                    "username": "string",
                    "password": "string",
                    "phone_number": "string",
                },
                request_only=True,
            )
        ],
    )
    def create_user(self, request, *args, **kwargs):
        if "profile_pic" in request.data.keys():
            if request.data["profile_pic"] in ["", None, "null"] or isinstance(
                request.data["profile_pic"], str
            ):
                request.data.pop("profile_pic")

        request.data["role"] = UserRole.USER.value

        # Hash and secure password
        if "password" in request.data.keys():
            try:
                validate_password(request.data["password"])
                request.data["password"] = make_password(request.data["password"])
            except ValidationError:
                return Response({"message": "Given password is too weak."}, 400)

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User created"}, 201)
        else:
            return Response(serializer.errors, 400)

    @extend_schema(
        tags=["User"],
        examples=[
            OpenApiExample(
                "Create Admin",
                value={
                    "first_name": "string",
                    "last_name": "string",
                    "email": "user@example.com",
                    "username": "string",
                    "password": "string",
                    "phone_number": "string",
                },
                request_only=True,
            )
        ],
    )
    def create_admin(self, request, *args, **kwargs):
        if "profile_pic" in request.data.keys():
            if request.data["profile_pic"] in ["", None, "null"] or isinstance(
                request.data["profile_pic"], str
            ):
                request.data.pop("profile_pic")

        request.data["role"] = UserRole.ADMIN.value
        request.data["is_superuser"] = True
        request.data["is_staff"] = True

        # Hash and secure password
        if "password" in request.data.keys():
            try:
                validate_password(request.data["password"])
                request.data["password"] = make_password(request.data["password"])
            except ValidationError:
                return Response({"message": "Given password is too weak."}, 400)

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Admin created"}, 201)
        else:
            return Response(serializer.errors, 400)

    @extend_schema(
        tags=["User"],
        examples=[
            OpenApiExample(
                "Update User",
                value={
                    "first_name": "string",
                    "last_name": "string",
                    "phone_number": "string",
                    "profile_pic": "file",
                    "date_of_birth": "1996-10-25",
                },
                request_only=True,
            )
        ],
    )
    def update_user(self, request, *args, **kwargs):
        if request.user.role != UserRole.ADMIN.value:
            return Response(
                {"message": "Unauthorize access ! Only admin can update users info"}
            )
        instance = self.get_queryset().filter(id=kwargs["id"]).first()
        if not instance:
            return Response({"message": "User not found"}, 400)

        if "profile_pic" in request.data.keys():
            if request.data["profile_pic"] in ["", None, "null"] or isinstance(
                request.data["profile_pic"], str
            ):
                request.data.pop("profile_pic")

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(
            data=request.data, instance=instance, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User updated"}, 202)
        else:
            return Response(serializer.errors, 400)

    @extend_schema(
        tags=["User"],
        examples=[
            OpenApiExample(
                "Update Profile",
                value={
                    "first_name": "string",
                    "last_name": "string",
                    "phone_number": "string",
                    "profile_pic": "file",
                    "date_of_birth": "1996-10-25",
                },
                request_only=True,
            )
        ],
    )
    def update_my_profile(self, request, *args, **kwargs):
        instance = self.get_queryset().filter(id=kwargs["id"]).first()
        if not instance:
            return Response({"message": "User not found"}, 400)

        if instance.id != request.user.id:
            return Response({"message": "Access denied"}, 406)

        if "profile_pic" in request.data.keys():
            if request.data["profile_pic"] in ["", None, "null"] or isinstance(
                request.data["profile_pic"], str
            ):
                request.data.pop("profile_pic")

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(
            data=request.data, instance=instance, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Profile updated"}, 202)
        else:
            return Response(serializer.errors, 400)

    @extend_schema(tags=["User"])
    def user_list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        serializer_class = (
            self.get_serializer_class()
            if self.serializer_class
            else self.serializer_class
        )
        if page is not None:
            serializer = serializer_class(page, many=True, context={"request": request})
            return self.get_paginated_response(serializer.data)
        return Response(serializer_class(queryset, many=True).data, 200)

    @extend_schema(tags=["User"])
    def user_retrieve(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer_class = self.get_serializer_class()
        instance = queryset.filter(id=kwargs["id"]).first()
        if instance:
            return Response(
                serializer_class(instance, context={"request": request}).data, 200
            )
        else:
            return Response("Invalid id", 400)
