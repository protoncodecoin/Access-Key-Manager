from rest_framework import permissions


class MicroFocusAdminAPIPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if (
            request.user
            and request.user.is_authenticated
            and request.user.is_micro_focus_admin
            and request.user.is_staff
            and request.user.groups.filter(name="MicroAdmin").exists()
            or request.user.is_superuser
        ):
            return True
