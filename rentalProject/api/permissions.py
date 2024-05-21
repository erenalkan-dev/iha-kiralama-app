
from rest_framework.permissions import BasePermission

class IsAuthenticatedForNonPost(BasePermission):
    """
    The request is not authenticated for POST requests only.
    """

    def has_permission(self, request, view):
        if request.method != 'POST':
            return request.user and request.user.is_authenticated
        return True  # Diğer yöntemlere izin ver
    
class IsAuthenticatedForNonGet(BasePermission):
    """
    The request is not authenticated for GET requests only.
    """

    def has_permission(self, request, view):
        if request.method != 'GET':
            return request.user and request.user.is_authenticated
        return True  # Diğer yöntemlere izin ver