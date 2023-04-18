from rest_framework.permissions import BasePermission


class IsLeadNotGET(BasePermission):
    def has_permission(self, request, view):
        if request.method == "GET":
            return True
        elif request.user.is_lead:
            return True
        return False


class IsLead(BasePermission):
    def has_permission(self, request, view):
        print(request.user.is_lead)
        if request.user.is_lead:
            print(request.user)
            return True
        return False
