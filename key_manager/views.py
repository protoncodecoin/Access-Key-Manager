from django.views import generic, View
from django.shortcuts import redirect
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.utils import timezone

from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework import authentication

from .models import AccessKey
from .serializers import AccessKeySerializer
from .permissions import MicroFocusAdminAPIPermission

# Create your views here.


class OwnerMixin:
    """
    filtered based on the user
    """

    def get_queryset(self):
        # check the status of the latest key provided
        latest_key = super().get_queryset().filter(user=self.request.user).first()

        # check if the latest key exists and if it has expired
        if latest_key and latest_key.expiry_date < timezone.now():
            # update the status to expired
            latest_key.status = AccessKey.Status.EXPIRED
            latest_key.save()

        # Retrieve all keys for the user
        qs = super().get_queryset().filter(user=self.request.user)

        return qs


class MangeKeysListView(OwnerMixin, LoginRequiredMixin, generic.ListView):
    """
    List keys related to the requested user
    """

    paginate_by = 3
    model = AccessKey
    context_object_name = "keys"
    template_name = "key_manager/dashboard.html"


# List of drecorators to decorate the CreateNewKey class
decorators = [require_POST, login_required]


@method_decorator(decorators, name="dispatch")
class CreateNewKey(View):

    def post(self, request, *args, **kwargs):
        user = request.user
        key_obj = AccessKey.objects.filter(
            status=AccessKey.Status.ACTIVE, user=request.user
        ).exists()
        if not key_obj:
            AccessKey.objects.create(user=user, status=AccessKey.Status.ACTIVE)
            messages.success(request, "New key was created successfully")
            return redirect("key_manager:dashboard")

        messages.error(request, "There is already an active key")
        return redirect("key_manager:dashboard")


class CheckKeyStatus(APIView):
    """
    View to check and return key based on the status.
    """

    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [MicroFocusAdminAPIPermission]

    def get(self, request, email, format=None):
        user_model = get_user_model()
        try:
            user = user_model.objects.get(email=email)
            active_key = AccessKey.activeKeys.filter(user=user).first()
            if active_key:
                if not active_key.expiry_date < timezone.now():
                    serializer = AccessKeySerializer(active_key)
                    return Response(serializer.data, status=status.HTTP_200_OK)
                else:
                    # update the status to expired
                    active_key.status = AccessKey.Status.EXPIRED
                    active_key.save()
                    return Response(
                        {"error": "No active Key found"},
                        status=status.HTTP_404_NOT_FOUND,
                    )

            return Response(
                {"error": "No active Key found"}, status=status.HTTP_404_NOT_FOUND
            )
        except user_model.DoesNotExist:
            return Response(
                {"error": "User not found"}, status=status.HTTP_404_NOT_FOUND
            )
