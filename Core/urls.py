from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path("register/", views.signup, name="signup"),
    path("login/", views.login_user, name="login"),
    # password reset urls
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path(
        "password-reset/", auth_views.PasswordResetView.as_view(), name="password_reset"
    ),
    path(
        "password-reset/done/",
        auth_views.PasswordResetDoneView.as_view(),
        name="password_reset_done",
    ),
    path(
        "password-reset-confirm/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path(
        "password-reset-complete/",
        auth_views.PasswordResetCompleteView.as_view(),
        name="password_reset_complete",
    ),
    # # activate account
    path("activate/<uidb64>/<token>/", views.activate, name="activate"),
]
