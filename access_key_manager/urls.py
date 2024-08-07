"""
URL configuration for access_key_manager project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include


admin.site.site_title = "Micro Focus Inc"
admin.site.site_header = "Micro Focus Inc."
admin.site.index_title = "Key Manager Administration"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("key_manager.urls", namespace="key_manager")),
    path("accounts/", include("Core.urls")),
]
