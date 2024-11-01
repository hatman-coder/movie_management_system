from rest_framework import serializers
from ..models import *


class MovieCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = [
            "name",
            "description",
            "released_at",
            "duration",
            "genre",
            "language",
            "created_by",
        ]


class MovieUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ["name", "description", "released_at", "duration", "genre", "language", "updated_at"]


class MovieListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ["id", "name", "description", "genre", "avg_rating", "total_rating"]


class MovieRetrieveSerializer(serializers.ModelSerializer):
    created_by = serializers.CharField(source="created_by.get_full_name")

    class Meta:
        model = Movie
        fields = [
            "id",
            "description",
            "released_at",
            "duration",
            "genre",
            "created_by",
            "avg_rating",
            "total_rating",
            "language",
            "updated_at",
        ]


class SubmitRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ["user", "movie", "rating"]


class UpdateRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ["rating"]


class RatedMovieListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ["id", "movie", "rating", "updated_at"]


class ReportMovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportedMovie
        fields = ["id", "movie", "reported_by", "reason", "created_at"]


class ReportedMovieListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportedMovie
        fields = [
            "id",
            "movie",
            "reported_by",
            "reason",
            "created_at",
            "acknowledged",
            "admin_approval"
        ]


class ReportReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportedMovie
        fields = ["acknowledged", "admin_approval"]
