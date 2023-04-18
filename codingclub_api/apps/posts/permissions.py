from rest_framework.permissions import BasePermission


class IsAuthenticatedNotGET(BasePermission):
    def has_permission(self, request, view):
        if str(request.user) == "AnonymousUser" and request.method == "GET":
            return True
        elif request.user.is_authenticated:
            return True
        return False
