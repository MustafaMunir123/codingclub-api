from rest_framework.permissions import BasePermission


class IsLeadNotGET(BasePermission):
    def has_permission(self, request, view):
        if request.method == "GET":
            return True
        if request.user.is_lead:
            return True
        return False


class IsLead(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_lead:
            return True
        return False
