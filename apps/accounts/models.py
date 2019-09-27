import uuid
from datetime import timedelta
from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    # automatic
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    email = models.EmailField(unique=True)

    updated_at = models.DateTimeField(auto_now=True, verbose_name="mise à jour")

    start_balance = models.DurationField(
        default=timedelta(), verbose_name="solde de départ"
    )

    REQUIRED_FIELDS = ["email"]

    def __str__(self):
        if self.first_name and self.last_name:
            return "{} {}".format(self.first_name, self.last_name)
        else:
            return self.username

    class Meta:
        verbose_name = "utilisateur"
        verbose_name_plural = "utilisateurs"
        ordering = ["username"]
