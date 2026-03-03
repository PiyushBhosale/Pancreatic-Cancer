from django.db import models
from django.conf import settings


class Prediction(models.Model):

    STATUS_CHOICES = [
        ('Cancer', 'Cancer'),
        ('No Cancer', 'No Cancer'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='predictions'
    )

    uploaded_image = models.ImageField(upload_to='pancreas_images/')

    predicted_label = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        null=True,
        blank=True
    )

    confidence_score = models.FloatField(
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)