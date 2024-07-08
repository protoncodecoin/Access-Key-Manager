from django.test import TestCase
from django.contrib.auth import get_user_model

# Create your tests here.


class UserManagerTests(TestCase):

    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(email="test@test.com", password="test123")
        self.assertEqual(user.email, "test@test.com")
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_superuser)
        self.assertFalse(user.is_staff)

        try:
            # Username is set to None for AbstractUser
            self.assertIsNone(self.user.username)
        except AttributeError:
            pass

        with self.assertRaises(TypeError):
            User.objects.create_user()

        with self.assertRaises(TypeError):
            User.objects.create_user(email="")

        with self.assertRaises(ValueError):
            User.objects.create_user(email="", password="hi")

    def test_create_superuser(self):
        User = get_user_model()
        admin_user = User.objects.create_superuser(
            email="admin@test.com", password="test123"
        )
        self.assertEqual(admin_user.email, "admin@test.com")
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)
        self.assertTrue(admin_user.is_active)

        try:
            # username is None for Abstract User
            self.assertIsNone(admin_user.username)
        except AttributeError:
            pass

        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                email="testadmin@admin.com", password="test123", is_superuser=False
            )
