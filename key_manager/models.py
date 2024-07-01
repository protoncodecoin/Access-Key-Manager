from datetime import timedelta
from django.db import models
from django.utils import timezone
from django.conf import settings

import uuid


class ActiveKeyManager(models.Manager):
    def get_queryset(self) -> models.QuerySet:
        return super().get_queryset().filter(status=AccessKey.Status.ACTIVE)


# Create your models here.
class AccessKey(models.Model):
    """
    Table to manage Keys
    """

    class Status(models.TextChoices):

        ACTIVE = "active", "Active"
        EXPIRED = "expired", "Expired"
        REVOKED = "revoked", "Revoked"

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    key = models.UUIDField(default=uuid.uuid4, editable=False)
    status = models.CharField(max_length=7, choices=Status.choices)
    procurement_date = models.DateTimeField(default=None)
    expiry_date = models.DateTimeField(default=None)
    updated_on = models.DateTimeField(auto_now=True)

    objects = models.Manager()  # The default manager
    activeKeys = ActiveKeyManager()  # Returns the active key

    class Meta:
        ordering = ["-procurement_date"]
        indexes = [
            models.Index(
                fields=[
                    "status",
                    "procurement_date",
                ]
            ),
        ]
        verbose_name_plural = "Access Key"

    def __str__(self):
        return self.status

    def save(self, *args, **kwargs):
        if self.expiry_date is None:
            self.expiry_date = timezone.now() + timedelta(days=30)

        if self.procurement_date is None:
            self.procurement_date = timezone.now()

        super(AccessKey, self).save(*args, **kwargs)
