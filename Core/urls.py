from django.urls import path
from .import views
from django.contrib.auth import views as auth_views

app_name="users"

urlpatterns = [

    path("register/", views.signup, name="signup"),
    path("login/", views.user_login, name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("passwordreset/", auth_views.PasswordResetView.as_view(), name="reset_password"),
    path("passwordreset/done/", auth_views.PasswordResetDoneView.as_view(), name="reset_password_done" ),
    # path("account/passwordreset/confirm/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(), name="reset_password_confirm"),
    path("passwordreset/complete/", auth_views.PasswordResetCompleteView.as_view(), name="reset_password_complete"),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
]