import uuid
from datetime import timedelta
from decimal import Decimal
from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
import simple_history
from simple_history.models import HistoricalRecords
from accounts.models import CustomUser

TEXT_MAX_LENGTH = 1000
DAILY_WORKING_TIME = timedelta(hours=7)


class Location(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="création")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="mise à jour")
    history = HistoricalRecords()

    title = models.CharField(max_length=TEXT_MAX_LENGTH, verbose_name="titre")
    comment = models.CharField(
        null=True, blank=True, max_length=TEXT_MAX_LENGTH, verbose_name="commentaire"
    )

    def __str__(self):
        return "{}".format(self.title)

    class Meta:
        verbose_name = "localisation"
        verbose_name_plural = "localisations"
        ordering = ("created_at",)


def heures(td):
    return "h".join(str(td).split(":")[:2])


class Task(MPTTModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="création")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="mise à jour")
    # history = HistoricalRecords()

    parent = TreeForeignKey(
        "self", on_delete=models.PROTECT, null=True, blank=True, related_name="children"
    )

    title = models.CharField(max_length=TEXT_MAX_LENGTH, verbose_name="titre")
    comment = models.CharField(
        null=True, blank=True, max_length=TEXT_MAX_LENGTH, verbose_name="commentaire"
    )

    @property
    def duration(self):
        t = timedelta()
        for activity in self.activities.all():
            t += activity.duration
        return t

    @property
    def total(self):
        t = timedelta()
        for activity in self.get_descendants(include_self=True):
            t += activity.duration
        return t

    def __str__(self):
        return "{} (total : {})".format(self.title, heures(self.total))

    class Meta:
        verbose_name = "tâche"
        verbose_name_plural = "tâches"


simple_history.register(Task)


class Activity(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="création")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="mise à jour")
    history = HistoricalRecords()

    user = models.ForeignKey(
        CustomUser,
        on_delete=models.PROTECT,
        related_name="activities",
        related_query_name="activity",
        verbose_name="utilisateur",
    )
    task = models.ForeignKey(
        Task,
        on_delete=models.PROTECT,
        related_name="activities",
        related_query_name="activity",
        verbose_name="tâche",
    )

    date = models.DateField()
    duration = models.DurationField(default=timedelta(hours=1), verbose_name="durée")

    location = models.ForeignKey(
        Location,
        on_delete=models.PROTECT,
        related_name="activities",
        related_query_name="activity",
        verbose_name="localisation",
    )
    is_teleworking = models.BooleanField(default=False, verbose_name="télétravail")
    is_business_trip = models.BooleanField(default=False, verbose_name="déplacement")

    comment = models.CharField(
        null=True, blank=True, max_length=TEXT_MAX_LENGTH, verbose_name="commentaire"
    )

    def __str__(self):
        return "{} ({} heures le {})".format(self.task, self.duration, self.date)

    class Meta:
        verbose_name = "activité"
        verbose_name_plural = "activités"
        ordering = ("-date",)


class Leave(models.Model):
    CONGES = "C"
    RECUP = "R"
    FERIE = "F"
    MALADIE = "M"
    SANS_SOLDE = "S"
    AUTRE = "A"

    TYPE_CHOICES = [
        (CONGES, "congé payé"),
        (RECUP, "récupération"),
        (FERIE, "jour ferié"),
        (MALADIE, "arrêt maladie"),
        (SANS_SOLDE, "congé sans solde"),
        (AUTRE, "autre ..."),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="création")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="mise à jour")
    history = HistoricalRecords()

    user = models.ForeignKey(
        CustomUser,
        on_delete=models.PROTECT,
        related_name="leaves",
        related_query_name="leave",
        verbose_name="utilisateur",
    )

    type = models.CharField(
        max_length=1,
        choices=TYPE_CHOICES,
        default=CONGES,
        verbose_name="type d'absence",
    )

    date = models.DateField()
    duration = models.DurationField(default=DAILY_WORKING_TIME, verbose_name="durée")

    comment = models.CharField(
        null=True, blank=True, max_length=TEXT_MAX_LENGTH, verbose_name="commentaire"
    )

    def __str__(self):
        return "{} ({} heures le {})".format(
            self.get_type_display(), self.duration, self.date
        )

    class Meta:
        verbose_name = "absence"
        verbose_name_plural = "absences"
        ordering = ("-date",)
