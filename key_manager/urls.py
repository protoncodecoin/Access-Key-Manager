from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from . import views

app_name = "key_manager"

urlpatterns = [
    path("", views.MangeKeysListView.as_view(), name="dashboard"),
    path("create/", views.CreateNewKey.as_view(), name="create_key"),
    # endpoints
    path(
        "api/check_key_status/<str:email>/",
        views.CheckKeyStatus.as_view(),
        name="check_key_status",
    ),
    path(
        "api/token/",
        views.MicroFocusTokenObtainPairView.as_view(),
        name="token_obtain_pair",
    ),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refesh"),
]
