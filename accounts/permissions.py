from rest_framework.permissions import BasePermission

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.groups.filter(name="Admin").exists()

class IsAnalyst(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.groups.filter(name="Analyst").exists()
