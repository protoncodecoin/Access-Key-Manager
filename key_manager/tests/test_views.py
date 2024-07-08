from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse

from key_manager.models import AccessKey


class DashboardTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create a test user
        cls.user = get_user_model().objects.create_user(
            email="test@test.com", password="@64!64#23fghd"
        )

        # Create 5 keys for pagination
        number_of_keys = 6
        for key in range(number_of_keys):
            if key == 5:
                AccessKey.objects.create(user=cls.user, status=AccessKey.Status.ACTIVE)
            else:
                AccessKey.objects.create(user=cls.user, status=AccessKey.Status.REVOKED)

    def setUp(self):
        self.client = Client()

    def test_user_creation(self):
        # Ensure the user is created correctly
        """
        Test to check creating of user is successful
        """
        try:
            get_user_model().objects.get(email="test@test.com")

        except get_user_model().DoesNotExist:
            self.fail("User creation failed in setUpTestData")

    def test_login(self):
        """
        Test to check active user logging in successful
        """
        # Ensure the user is created correctly
        try:
            get_user_model().objects.get(email="test@test.com")
        except get_user_model().DoesNotExist:
            self.fail("User creation failed in setUpTestData")

        # Attempt to log in the user
        login = self.client.login(email="test@test.com", password="@64!64#23fghd")

        self.assertTrue(login)

    def test_redirect_if_not_logged_in(self):
        """
        Test unauthenticated users are redirected to the login page
        """
        response = self.client.get("/")
        self.assertRedirects(response, "/accounts/login/?next=/")

    def test_url_available_by_name(self):
        """
        Test url name for url path is available
        """
        login = self.client.login(email="test@test.com", password="@64!64#23fghd")
        self.assertTrue(login)
        response = self.client.get(reverse("key_manager:dashboard"))
        self.assertEqual(response.status_code, 200)

    def test_home_template_name_correct(self):
        """
        Test correct template is rendered when redirected to the home page.
        """
        login = self.client.login(email="test@test.com", password="@64!64#23fghd")

        self.assertTrue(login)
        response = self.client.get(reverse("key_manager:dashboard"))
        self.assertTemplateUsed(response, "key_manager/dashboard.html")

    def test_login_template_name_correct(self):
        """
        Test correct template is rendered when redirected to the login page.
        """

        response = self.client.get(reverse("login"))
        self.assertTemplateUsed(response, "registration/login.html")

    def test_register_template_name_correct(self):
        """
        Test correct template is rendered when at the signup page
        """

        response = self.client.get(reverse("signup"))
        self.assertTemplateUsed(response, "registration/signup.html")

    def test_paginate_lists_of_keys(self):
        """
        Test keys returned from the view is paginated and is paginated by three (3)
        """
        login = self.client.login(email="test@test.com", password="@64!64#23fghd")
        self.assertTrue(login)
        response = self.client.get(reverse("key_manager:dashboard"))
        self.assertEqual(response.status_code, 200)

        response = self.client.get(reverse("key_manager:dashboard") + "?page=2")
        self.assertEqual(response.status_code, 200)
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"] is True)
        self.assertEqual(len(response.context["keys"]), 3)

    def test_create_new_key_while_active_key_present_fails(self):
        """
        Test creating key while there is an already active key fails
        """
        login = self.client.login(email="test@test.com", password="@64!64#23fghd")
        self.assertTrue(login)
        response = self.client.post(reverse("key_manager:create_key"))
        self.assertEqual(response.status_code, 302)

        qs = AccessKey.objects.all()
        active_keys = qs.filter(status=AccessKey.Status.ACTIVE, user=self.user.id)

        self.assertEqual(len(qs), 6)
        self.assertEqual(len(active_keys), 1)

    def test_create_new_key_redirect_user_to_dashboard(self):
        """
        Test after creating an active key redirects user to the dashboard
        """
        login = self.client.login(email="test@test.com", password="@64!64#23fghd")
        self.assertTrue(login)
        response = self.client.post(reverse("key_manager:create_key"))
        self.assertEqual(response.status_code, 302)
