from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone

from datetime import datetime, timedelta

from key_manager.models import KeyManager
import uuid

# Create your tests here.
class KeyManagerTests(TestCase):

    def test_create_key(self):
        """
        Test to create new Key
        """
        user = get_user_model().objects.create_user(email="test@test.com", password="test")
        unique_id = uuid.uuid4()
        issued_key = KeyManager.objects.create(user=user, key=unique_id, status=KeyManager.Status.ACTIVE, procurement_date=timezone.now(), expiry_date=timezone.now() + timedelta(days=2))

        self.assertEqual(issued_key.key, unique_id)
        self.assertEqual(issued_key.status, KeyManager.Status.ACTIVE)
        

