from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
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
        """
        set up new staff user for each test.
        """
        # instantiate client
        self.client = APIClient()

        # create a staff user
        self.staff_user = get_user_model().objects.create_user(
            email="staff_user@test.com", password="staff_password"
        )
        self.staff_user.is_staff = True
        self.staff_user.is_micro_focus_admin = True
        self.staff_user.save()

        staff_group = Group.objects.create(name="MicroAdmin")
        staff_group.save()

        self.staff_user.groups.add(staff_group)

    def test_check_if_staff_in_db(self):
        """
        Test to check if the staff user created has the right privilages and has the correct status
        """
        existing_user = get_user_model().objects.get(email="staff_user@test.com")

        self.assertTrue(existing_user.email, "staff_user@test.com")
        self.assertTrue(self.staff_user.is_staff)
        self.assertTrue(self.staff_user.is_micro_focus_admin)

    def test_check_active_key_status_return_200(self):
        """
        Test to check active keys return a status of 200 (ok)
        """

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
        """
        Test to check revoked keys return a status of 404 (not found)
        """

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
        """
        Test to check expired keys return a status of 404 (not found)
        """

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
        """
        Test to check unathorizied users return a status of 403 (unauthorized).
        """

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
        """
        Test to check if the status of a key is checked before being returned
        """
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

    def test_check_login_api_endpoint_with_valid_credientials_return_token(self):
        """
        Test to check valid post request sent to the token endpoint returns the token
        """
        url = reverse("key_manager:token_obtain_pair")

        data = {"email": self.staff_user.email, "password": "staff_password"}

        response = self.client.post(url, data=data)
        self.assertTrue(response.status_code, 200)
        self.assertIn("refresh", response.data)
        self.assertIn("access", response.data)

    def test_login_endpoint_without_valid_credentials_return_error(self):
        """
        Test to check in-valid post request sent to the token endpoint returns error
        """
        url = reverse("key_manager:token_obtain_pair")

        data = {"email": self.staff_user.email, "password": "wrong_password"}

        response = self.client.post(url, data=data)
        self.assertTrue(response.status_code, 200)
        self.assertIn("detail", response.data)
        self.assertEqual(
            response.data["detail"],
            "No active account found with the given credentials",
        )

    def test_authorization_header_with_token_return_resources(self):
        """
        Test to check valid post request sent to the token endpoint returns the token and a valid get request to the check_status_key with the authorization token returns the resources
        """
        login_url = reverse("key_manager:token_obtain_pair")

        data = {"email": self.staff_user.email, "password": "staff_password"}

        response = self.client.post(login_url, data=data)
        self.assertTrue(response.status_code, 200)
        self.assertIn("refresh", response.data)
        self.assertIn("access", response.data)

        access_token = response.data["access"]

        headers = {"Authorization": f"Bearer {access_token}"}
        endpoint_url = reverse(
            "key_manager:check_key_status", kwargs={"email": self.active_key_user.email}
        )

        key_response = self.client.get(endpoint_url, headers=headers)
        self.assertTrue(key_response.status_code, 200)
        self.assertIn("key", key_response.data)
        self.assertIn("status", key_response.data)
        self.assertIn("procurement_date", key_response.data)
        self.assertIn("expiry_date", key_response.data)
        self.assertNotIn("updated_on", key_response.data)

    def test_authorization_header_without_token_return_403(self):
        """
        Test to check invalid get request to the check_status_key with the authorization token returns the resources
        """
        endpoint_url = reverse(
            "key_manager:check_key_status", kwargs={"email": self.active_key_user.email}
        )

        key_response = self.client.get(endpoint_url)
        self.assertTrue(key_response.status_code, 403)
        self.assertNotIn("key", key_response.data)
        self.assertNotIn("status", key_response.data)
        self.assertNotIn("procurement_date", key_response.data)
        self.assertNotIn("expiry_date", key_response.data)
