from typing import Iterable
from abstract.base_model import BaseModel
from django.db import models
from django.db.models import Avg
from apps.user.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from external.enum import AdminApproval


class Movie(BaseModel):
    name = models.CharField(max_length=150)
    description = models.TextField()
    released_at = models.DateField()
    duration = models.PositiveIntegerField(help_text="Duration in minutes")
    genre = models.CharField(max_length=50)
    created_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="movies_creator"
    )
    avg_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    total_rating = models.PositiveIntegerField(default=0)
    language = models.CharField(max_length=50)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]


class Rating(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="ratings")
    rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )

    def save(self, *args, **kwargs):
        # Saving the rating instance first
        super().save(*args, **kwargs)

        # Calculating the average rating and total count for the movie
        avg_rating = self.movie.ratings.aggregate(Avg("rating"))["rating__avg"]
        total_ratings = self.movie.ratings.count()

        # Updating the movie's avg_rating and total_rating fields
        self.movie.avg_rating = avg_rating or 0.00
        self.movie.total_rating = total_ratings
        self.movie.save(update_fields=["avg_rating", "total_rating"])

    class Meta:
        ordering = ["-created_at"]


class ReportedMovie(BaseModel):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    reported_by = models.ForeignKey(User, on_delete=models.CASCADE)
    reason = models.TextField()
    acknowledged = models.BooleanField(default=False)
    admin_approval = models.CharField(
        max_length=50,
        choices=AdminApproval.choices(),
        default=AdminApproval.PENDING.value,
    )

    class Meta:
        ordering = ["-created_at"]
