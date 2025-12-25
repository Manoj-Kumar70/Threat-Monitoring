from rest_framework.permissions import BasePermission

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'ADMIN'

class IsAnalystReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in ['GET']:
            return request.user.role in ['ADMIN', 'ANALYST']
        return request.user.role == 'ADMIN'
