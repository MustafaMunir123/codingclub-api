from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        # print(request.user.is_admin)
        if request.method == "POST" or request.method == "GET":
            if request.user.is_admin:
                return True
        return False


class IsAuthenticatedNotPOST(BasePermission):
    def has_permission(self, request, view):
        # print(str(request.user))
        if str(request.user) == "AnonymousUser" and request.method == "POST":
            return True
        elif request.user.is_authenticated:
            return True
        return False
