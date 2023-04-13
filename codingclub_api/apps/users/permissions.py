from rest_framework.permissions import BasePermission


class IsSuperAdmin(BasePermission):
    def has_permission(self, request, view):
        if request.method == "POST":
            if request.user.is_admin:
                return True
        return False
