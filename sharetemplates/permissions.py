from rest_framework import permissions


class TemplatePermission(permissions.BasePermission):
    """
    Custom permission for Template model:
    - Normal users can list and retrieve templates
    - Staff users can create, update, delete templates
    """

    def has_permission(self, request, view):
        # Allow read permissions for any authenticated user
        if request.method in permissions.SAFE_METHODS:
            return request.user.is_authenticated

        # Write permissions only for staff users
        return request.user.is_authenticated and request.user.is_staff

    def has_object_permission(self, request, view, obj):
        # Read permissions for any authenticated user
        if request.method in permissions.SAFE_METHODS:
            return request.user.is_authenticated

        # Write permissions only for staff users
        return request.user.is_authenticated and request.user.is_staff
