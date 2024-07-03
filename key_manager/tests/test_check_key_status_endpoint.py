from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from datetime import timedelta
from django.utils import timezone

from rest_framework.test import APIClient, APITestCase

from key_manager.models import AccessKey


class KeyStatusEndpoinTest(APITestCase):

    @classmethod
    def setUpTestData(cls):
        # Create a test user
        cls.active_key_user = get_user_model().objects.create_user(
            email="test@test.com", password="@64!64#23fghd"
        )

        cls.revoked_key_user = get_user_model().objects.create_user(
            email="test1@test.com", password="@64!64rert"
        )

        cls.expired_key_user = get_user_model().objects.create_user(
            email="test2@test.com", password="@yt!64rert"
        )

        # Create an active test access key
        AccessKey.objects.create(
            user=cls.active_key_user, status=AccessKey.Status.ACTIVE
        )

        # Create a revoked test access key
        AccessKey.objects.create(
            user=cls.revoked_key_user, status=AccessKey.Status.REVOKED
        )

        # Create a expired test access key
        AccessKey.objects.create(
            user=cls.revoked_key_user, status=AccessKey.Status.EXPIRED
        )

    def setUp(self):
        # instantiate client
        self.client = APIClient()

        # create a staff user
        self.staff_user = get_user_model().objects.create_user(
            email="staff_user@test.com", password="staff_password"
        )
        self.staff_user.is_staff = True
        self.staff_user.save()

        content_type = ContentType.objects.get_for_model(AccessKey)
        access_key_permission = Permission.objects.filter(content_type=content_type)

        staff_group = Group.objects.create(name="MicroAdmin")
        staff_group.save()

        for perm in access_key_permission:
            if (
                perm.codename == "change_access_key"
                or perm.codename == "view_access_key"
            ):
                staff_group.permissions.add(perm)

        self.staff_user.groups.add(staff_group)

    def test_check_if_staff_in_db(self):
        existing_user = get_user_model().objects.get(email="staff_user@test.com")

        self.assertTrue(existing_user.email, "staff_user@test.com")
        self.assertTrue(self.staff_user.is_staff)

    def test_check_active_key_status_return_200(self):

        url = reverse(
            "key_manager:check_key_status", kwargs={"email": self.active_key_user.email}
        )

        login = self.client.login(
            email="staff_user@test.com", password="staff_password"
        )

        response = self.client.get(url)

        self.assertTrue(login)
        self.assertEqual(response.status_code, 200)

    def test_check_revoked_key_status_return_404(self):

        url = reverse(
            "key_manager:check_key_status",
            kwargs={"email": self.revoked_key_user.email},
        )

        login = self.client.login(
            email="staff_user@test.com", password="staff_password"
        )

        response = self.client.get(url)
        self.assertTrue(login)
        self.assertEqual(response.status_code, 404)

    def test_check_expired_key_status_return_404(self):

        url = reverse(
            "key_manager:check_key_status",
            kwargs={"email": self.expired_key_user.email},
        )

        login = self.client.login(
            email="staff_user@test.com", password="staff_password"
        )

        response = self.client.get(url)
        self.assertTrue(login)
        self.assertEqual(response.status_code, 404)

    def test_unauthorized_user_return_403(self):

        url = reverse(
            "key_manager:check_key_status",
            kwargs={"email": self.active_key_user.email},
        )

        self.client.login(
            username="unauthorizeduser@test.com", password="testpassword123"
        )

        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

    def test_key_status_is_checked_before_returned(self):
        user2 = get_user_model().objects.create(
            email="user2@test.com", password="user281!@"
        )
        AccessKey.objects.create(
            user=user2,
            status=AccessKey.Status.ACTIVE,
            procurement_date=timezone.now() - timedelta(days=2),
            expiry_date=timezone.now(),
        )

        url = reverse(
            "key_manager:check_key_status",
            kwargs={"email": user2.email},
        )

        self.client.login(email="staff_user@test.com", password="staff_password")

        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
