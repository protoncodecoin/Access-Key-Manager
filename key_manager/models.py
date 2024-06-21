from datetime import timedelta
from django.db import models
from django.utils import timezone
from django.urls import reverse

import uuid

from Core.models import ITPersonnel


# Create your models here.
class KeyManager(models.Model):
    """
    Table to manage Keys
    """

    class Status(models.TextChoices):

        ACTIVE = "active", "Active"
        EXPIRED = "expired", "Expired"
        REVOKED = "revoked", "Revoked"
    

    user = models.ForeignKey(ITPersonnel, on_delete=models.CASCADE)
    key = models.UUIDField(default=uuid.uuid4, editable=False)
    status = models.CharField(max_length=7, choices=Status.choices)
    procurement_date = models.DateTimeField(default=timezone.now)
    expiry_date = models.DateTimeField(default=timezone.now() + timedelta(days=30))


    class Meta:
        ordering = ["-procurement_date"]
        indexes = [
            models.Index(fields=["status", "-procurement_date",]),
        ]
        verbose_name_plural = "KeyManager"


    def __str__(self):
        return self.status
    
    def get_absolute_url(self):
        return reverse("key_manager:key_details", args=[self.id])
    
    def is_active(self):
        return self.status == KeyManager.Status.ACTIVE
    
    def is_expired(self):
        return self.status == KeyManager.Status.EXPIRED
    
    def is_revoked(self):
        return self.status == KeyManager.Status.REVOKED