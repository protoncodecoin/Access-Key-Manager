from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.exceptions import PermissionDenied

from .models import AccessKey


class AccessKeySerializer(serializers.ModelSerializer):
    class Meta:
        model = AccessKey
        fields = [
            "key",
            "status",
            "procurement_date",
            "expiry_date",
        ]


class MicroFocusObtainPairSerializer(TokenObtainPairSerializer):
    """
    customize the claims to include the status of the user

    Returns:
        token with staff status of the user
    """

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # add custom claims
        token["is_micro_focus_admin"] = user.is_micro_focus_admin

        return token

    def validate(self, attrs):
        data = super().validate(attrs)

        # check if the user is MicroAdmin or superuser
        if not self.user.is_micro_focus_admin and not self.user.is_superuser:
            raise PermissionDenied("You do not have permission to obtain a token")

        return data
