"""
VEDA V2 — accounts permission classes

Role-based DRF permissions used across all VEDA API views.
Import these in any view that needs role enforcement.

Usage:
    class MyView(APIView):
        permission_classes = [IsAuthenticated, IsOwner]
"""

from rest_framework.permissions import BasePermission
from .models import UserRole


class IsOwner(BasePermission):
    """User must hold the OWNER role."""
    message = "Vehicle owner access required."

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.has_role(UserRole.OWNER)
        )


class IsWorkshopAdmin(BasePermission):
    """User must hold the WORKSHOP_ADMIN role."""
    message = "Workshop administrator access required."

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.has_role(UserRole.WORKSHOP_ADMIN)
        )


class IsMechanic(BasePermission):
    """User must hold the MECHANIC role."""
    message = "Mechanic access required."

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.has_role(UserRole.MECHANIC)
        )


class IsVedaAdmin(BasePermission):
    """User must hold the VEDA_ADMIN role."""
    message = "VEDA administrator access required."

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.has_role(UserRole.VEDA_ADMIN)
        )


class IsWorkshopMember(BasePermission):
    """User must be WORKSHOP_ADMIN or MECHANIC."""
    message = "Workshop member access required."

    def has_permission(self, request, view):
        if not (request.user and request.user.is_authenticated):
            return False
        return request.user.has_role(UserRole.WORKSHOP_ADMIN) or \
               request.user.has_role(UserRole.MECHANIC)


class IsOwnerOrWorkshopMember(BasePermission):
    """User must be an OWNER, WORKSHOP_ADMIN, or MECHANIC."""
    message = "Authentication required."

    def has_permission(self, request, view):
        if not (request.user and request.user.is_authenticated):
            return False
        allowed = {UserRole.OWNER, UserRole.WORKSHOP_ADMIN, UserRole.MECHANIC}
        return any(request.user.has_role(r) for r in allowed)
