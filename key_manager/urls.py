from django.urls import path

from . import views

app_name = "key_manager"

urlpatterns = [
    path("", views.MangeKeysListView.as_view(), name="dashboard"),
    # path("listkeys/", views.ListKeys.as_view(), name="list_keys"),
    path("create/", views.CreateNewKey.as_view(), name="create_key"),
    path(
        "api/check_key_status/<str:email>/",
        views.CheckKeyStatus.as_view(),
        name="check_key_status",
    ),
]
