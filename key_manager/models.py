from datetime import date
from django.db import models
from django.utils import timezone
import uuid

from Core.models import ITPersonnel


# Create your models here.
class KeyManager(models.Model):
    """
    Table to manage Keys
    """

    KEY_STATUS = (
        ("active", "Active"),
        ("expired", "Expired"),
        ("revoked", "Revoked"),
    )

    user = models.ForeignKey(ITPersonnel, on_delete=models.CASCADE)
    key = models.UUIDField(default=uuid.uuid4, editable=False)
    status = models.CharField(max_length=7, choices=KEY_STATUS)
    procurement_date = models.DateTimeField(default=timezone.now)
    expiry_date = models.DateTimeField()


    class Meta:
        ordering = ["-procurement_date"]
        indexes = [
            models.Index(fields=["status", "-procurement_date",]),
        ]
        verbose_name_plural = "KeyManager"


    def __str__(self):
        return self.status