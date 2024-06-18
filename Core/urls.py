from django.urls import path
from .import views
from django.contrib.auth import views as auth_views

app_name="users"

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("account/register/", views.signup, name="signup"),
    path("account/login/", views.user_login, name="login"),
    path("account/logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("account/passwordreset/", auth_views.PasswordResetView.as_view(), name="reset_password"),
    path("account/passwordreset/done/", auth_views.PasswordResetDoneView.as_view(), name="reset_password_done" ),
    # path("account/passwordreset/confirm/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(), name="reset_password_confirm"),
    path("account/passwordreset/complete/", auth_views.PasswordResetCompleteView.as_view(), name="reset_password_complete"),
    path('account/activate/<uidb64>/<token>/', views.activate, name='activate'),
]