from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


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
        token["is_micro_focus_admin"] = user.groups.filter(name="MicroAdmin").exists()

        return token
