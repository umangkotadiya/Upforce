from rest_framework.permissions import BasePermission

class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if (request.method == 'PUT' or request.method == 'PATCH') and obj.user == request.user:
            return True
        else:
            return False
