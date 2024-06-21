from django.urls import path

from . import views

app_name ="key_manager"

urlpatterns = [
        path("", views.MangeKeysListView.as_view(), name="dashboard"),
        path("<int:pk>/", views.DetailKeyView.as_view(), name="key_details"),
        path("create/", views.create_key, name="create_key"),
]