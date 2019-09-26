import uuid
from datetime import timedelta
from decimal import Decimal
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
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


class Project(MPTTModel):
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

    resources = models.ManyToManyField(
        CustomUser,
        through="Resource",
        through_fields=("project", "user"),
        related_name="projects",
        related_query_name="project",
        verbose_name="ressources",
    )

    @property
    def allotted_time(self):
        """
            temps alloué au projet = somme des durées des ressources
        """
        t = timedelta()
        for resource in Resource.objects.filter(project=self):
            t += resource.duration
        return t

    @property
    def total_allotted_time(self):
        """
            temps alloué cumulé pour le projet projet lui-même et de ses sous-projets
        """
        t = timedelta()
        for project in self.get_descendants(include_self=True):
            t += project.allotted_time
        return t

    @property
    def duration(self):
        """
            temps déjà passé sur le projet
        """
        t = timedelta()
        for activity in self.activities.all():
            t += activity.duration
        return t

    @property
    def total(self):
        """
            temps déjà passé sur le projet, sous-projets inclus
        """
        t = timedelta()
        for activity in self.get_descendants(include_self=True):
            t += activity.duration
        return t

    @property
    def level_text(self):
        """
            texte pour faciliter le formatage d'un arbre
        """
        message = ""
        if self.level:
            for i in range(self.level):
                message += "&nbsp;&bull;&nbsp;"
        return message

    @property
    def progression(self):
        # dernière valeur de « progression » en date pour les objets « Activity » liés au projet, si elle existe
        activities = Activity.objects.filter(
            project=self, progression__isnull=False
        ).order_by("-date")
        try:
            progression = activities[0].progression
        except:
            return 0

        return progression

    @property
    def total_progression(self):
        a = self.total.seconds
        b = a + self.total_remaining_time_needed.seconds
        if b == 0:
            return 0
        else:
            return int(100 * a / b)

    @property
    def is_completed(self):
        if self.progression == 100:
            return True
        else:
            return False

    @property
    def remaining_time_allotted(self):
        return self.allotted_time - self.duration

    @property
    def total_remaining_time_allotted(self):
        return self.total_allotted_time - self.total

    @property
    def remaining_time_needed(self):
        if self.progression == 0:
            return self.allotted_time
        return self.duration * (100 / self.progression - 1)

    @property
    def total_remaining_time_needed(self):
        t = timedelta()
        for project in self.get_descendants(include_self=True):
            t += project.remaining_time_needed
        return t

    @property
    def margin(self):
        return self.remaining_time_allotted - self.remaining_time_needed

    @property
    def total_margin(self):
        return self.total_remaining_time_allotted - self.total_remaining_time_needed

    def __str__(self):
        return "{} ({}%)".format(self.title, self.total_progression)

    class Meta:
        verbose_name = "projet"
        verbose_name_plural = "projets"


simple_history.register(Project)


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
    project = models.ForeignKey(
        Project,
        on_delete=models.PROTECT,
        related_name="activities",
        related_query_name="activity",
        verbose_name="projet",
    )

    date = models.DateField()
    duration = models.DurationField(default=timedelta(hours=1), verbose_name="durée")

    progression = models.IntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name="avancement (%)",
    )

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
        return "{} ({} heures le {})".format(self.project, self.duration, self.date)

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


class Resource(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="création")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="mise à jour")
    history = HistoricalRecords()

    user = models.ForeignKey(
        CustomUser, on_delete=models.PROTECT, verbose_name="utilisateur"
    )

    project = models.ForeignKey(
        Project, on_delete=models.PROTECT, verbose_name="projet"
    )

    # si la date est renseignée, cela bloque la capacité
    date = models.DateField(null=True, blank=True)
    duration = models.DurationField(default=DAILY_WORKING_TIME, verbose_name="durée")

    comment = models.CharField(
        null=True, blank=True, max_length=TEXT_MAX_LENGTH, verbose_name="commentaire"
    )

    def __str__(self):
        if self.date:
            return "{} heures de {} le {} sur le projet {})".format(
                self.duration, self.user, self.date, self.project
            )
        else:
            return "{} heures de {} sur le projet {})".format(
                self.duration, self.user, self.project
            )

    class Meta:
        verbose_name = "ressource"
        verbose_name_plural = "ressources"
        ordering = ("-date",)


class Capacity(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="création")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="mise à jour")
    history = HistoricalRecords()

    user = models.ForeignKey(
        CustomUser,
        on_delete=models.PROTECT,
        related_name="capacities",
        related_query_name="capacity",
        verbose_name="utilisateur",
    )

    date = models.DateField()
    duration = models.DurationField(default=DAILY_WORKING_TIME, verbose_name="durée")

    comment = models.CharField(
        null=True, blank=True, max_length=TEXT_MAX_LENGTH, verbose_name="commentaire"
    )

    def __str__(self):
        return "{} heures le {}".format(self.duration, self.date)

    class Meta:
        verbose_name = "capacité"
        verbose_name_plural = "capacités"
        ordering = ("-date",)
