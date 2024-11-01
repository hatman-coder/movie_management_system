import datetime
from rest_framework import viewsets
from ..models import *
from ..serializers.serializers_v1 import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from external.pagination import CustomPagination
from external.enum import UserRole
from drf_spectacular.utils import extend_schema, OpenApiExample


class MovieViewSet(viewsets.ModelViewSet):
    model_class = Movie
    serializer_class = MovieListSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    def get_queryset(self):
        return self.model_class.objects.all()

    def get_serializer_class(self):

        if self.action == "create_movie":
            return MovieCreateSerializer
        if self.action in ["my_movies", "movies_list"]:
            return MovieListSerializer
        if self.action == "update_movie":
            return MovieUpdateSerializer
        if self.action == "retrieve_movie":
            return MovieRetrieveSerializer
        else:
            return self.serializer_class

    @extend_schema(
        tags=["Movie"],
        examples=[
            OpenApiExample(
                "Create Movie",
                value={
                    "name": "Iron Man",
                    "description": "An epic science fiction adventure",
                    "released_at": "2024-01-15",
                    "duration": 130,
                    "genre": "Science Fiction",
                    "language": "English",
                },
                request_only=True,
            )
        ],
    )
    def create_movie(self, request, *args, **kwargs):
        request.data["created_by"] = request.user.id
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Movie created"}, 201)
        else:
            return Response(serializer.errors, 400)

    @extend_schema(tags=["Movie"])
    def my_movies(self, request, *args, **kwargs):
        queryset = self.get_queryset().filter(created_by=request.user.id)
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

    @extend_schema(tags=["Movie"])
    def movies_list(self, request, *args, **kwargs):
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

    @extend_schema(tags=["Movie"])
    def retrieve_movie(self, request, *args, **kwargs):
        instance = self.get_queryset().filter(id=kwargs["id"]).first()
        if not instance:
            return Response({"message": "Movie not found"}, 400)
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(instance)
        return Response(serializer.data, 200)

    @extend_schema(
        tags=["Movie"],
        examples=[
            OpenApiExample(
                "Update Movie",
                value={
                    "name": "Iron Man",
                    "description": "An epic science fiction adventure",
                    "released_at": "2024-01-15",
                    "duration": 130,
                    "genre": "Science Fiction",
                    "language": "English",
                },
                request_only=True,
            )
        ],
    )
    def update_movie(self, request, *args, **kwargs):
        instance = self.get_queryset().filter(id=kwargs["id"]).first()
        if not instance:
            return Response({"message": "Movie not found"}, 400)

        if str(instance.created_by) != str(request.user):
            return Response(
                {"message": "You are only permitted to update movies that you own"}, 406
            )
        request.data["updated_at"] = datetime.datetime.now()
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data, instance=instance)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Movie updated"}, 201)
        else:
            return Response(serializer.errors, 400)


class RatingViewSet(viewsets.ModelViewSet):
    model_class = Rating
    serializer_class = RatedMovieListSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    def get_queryset(self):
        return self.model_class.objects.all()

    def get_serializer_class(self):
        if self.action == "submit_rating":
            return SubmitRatingSerializer
        if self.action == "update_rating":
            return UpdateRatingSerializer
        if self.action == "rated_movie_list":
            return RatedMovieListSerializer
        else:
            return self.serializer_class

    @extend_schema(
        tags=["Rating Movie"],
        examples=[
            OpenApiExample(
                "Submit Rating",
                value={"movie": "uuid", "rating": "int between 1 to 5"},
                request_only=True,
            )
        ],
    )
    def submit_rating(self, request, *args, **kwargs):
        request.data["user"] = request.user.id
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Rating submitted"}, 201)
        else:
            return Response(serializer.errors, 400)

    @extend_schema(
        tags=["Rating Movie"],
        examples=[
            OpenApiExample(
                "Update Rating",
                value={"rating": "int between 1 to 5"},
                request_only=True,
            )
        ],
    )
    def update_rating(self, request, *args, **kwargs):
        instance = self.get_queryset().filter(id=kwargs["id"]).first()
        if not instance:
            return Response({"message": "Movies rank not found"}, 400)

        if str(instance.user) != str(request.user):
            return Response(
                {"message": "You are only permitted to update rank for the movies that you own"}, 406
            )

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data, instance=instance)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Rating updated"}, 202)
        else:
            return Response(serializer.errors, 400)

    @extend_schema(tags=["Rating Movie"])
    def rated_movie_list(self, request, *args, **kwargs):
        queryset = (
            self.get_queryset()
            if request.user.role == UserRole.ADMIN.value
            else self.get_queryset().filter(user=request.user.id)
        )
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


class ReportedMovieViewSet(viewsets.ModelViewSet):
    model_class = ReportedMovie
    serializer_class = ReportedMovieListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.model_class.objects.all()

    def get_serializer_class(self):
        if self.action == "report_movie":
            return ReportMovieSerializer
        if self.action == "reported_movie_list":
            return ReportedMovieListSerializer
        if self.action == "review_report":
            return ReportReviewSerializer
        else:
            return self.serializer_class

    @extend_schema(
        tags=["Report Movie"],
        examples=[
            OpenApiExample(
                "Submit Report",
                value={"movie": "uuid", "reason": "text"},
                request_only=True,
            )
        ],
    )
    def report_movie(self, request, *args, **kwargs):
        request.data["reported_by"] = request.user.id
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Report submitted"}, 201)
        else:
            return Response(serializer.errors, 400)

    @extend_schema(tags=["Report Movie"])
    def reported_movie_list(self, request, *args, **kwargs):
        queryset = (
            self.get_queryset()
            if request.user.role == UserRole.ADMIN.value
            else self.get_queryset().filter(reported_by=request.user.id)
        )
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

    @extend_schema(
        tags=["Report Movie"],
        examples=[
            OpenApiExample(
                "Review Report",
                value={"acknowledged": "bool", "admin_approval": "approved/rejected"},
                request_only=True,
            )
        ],
    )
    def review_report(self, request, *args, **kwargs):
        reported_movie_obj = self.get_queryset().filter(id=kwargs["id"]).first()
        if not reported_movie_obj:
            return Response({"message": "Invalid id"}, 400)

        if request.user.role != UserRole.ADMIN.value:
            return Response(
                {"message": "Report acknowledgement can only be modified by an Admin"},
                406,
            )

        serializer_class = self.get_serializer_class()
        request.data["acknowledged"] = True
        serializer = serializer_class(data=request.data, instance=reported_movie_obj)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Report updated"}, 202)
        else:
            return Response(serializer.errors, 400)
