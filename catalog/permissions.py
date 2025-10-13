from rest_framework import permissions

class IsAuthenticatedReadAndAdminWrite(permissions.BasePermission):
    """
    - Read (GET, HEAD, OPTIONS) only for authenticated users (seller or admin).
    - Write (POST, PUT, PATCH, DELETE) only for users with the 'admin' role.
    """
    def has_permission(self, request, view):
        # Allow read-only access for authenticated users
        if request.method in permissions.SAFE_METHODS:
            return request.user and request.user.is_authenticated
        
        # Allow write access only for admin users
        return request.user and request.user.is_authenticated and getattr(request.user, 'role', "") == 'admin'
