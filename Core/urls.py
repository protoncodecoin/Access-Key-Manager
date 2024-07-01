from django.urls import path
from . import views


app_name = "users"

urlpatterns = [
    path("register/", views.signup, name="signup"),
    path("login/", views.login_user, name="login"),
    # # activate account
    path("activate/<uidb64>/<token>/", views.activate, name="activate"),
]
