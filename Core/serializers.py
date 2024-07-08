from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class MicroFocusObtainPairSerializer(TokenObtainPairSerializer):
    """_summary_

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
