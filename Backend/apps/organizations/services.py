"""VEDA V2 — organizations service layer"""

import logging
from django.db import transaction
from apps.accounts.models import User, UserRole
from apps.accounts.services import assign_role
from .models import ServiceCentre, WorkshopMembership, Designation

logger = logging.getLogger("veda.organizations")


class OrganizationError(Exception):
    pass

class CentreNotFoundError(OrganizationError):
    pass

class MembershipError(OrganizationError):
    pass


@transaction.atomic
def register_service_centre(user: User, data: dict) -> ServiceCentre:
    """Any authenticated user can register a service centre."""
    centre = ServiceCentre.objects.create(
        name=data["name"],
        address=data["address"],
        city=data.get("city", ""),
        state=data.get("state", ""),
        contact_number=data["contact_number"],
        email=data.get("email", ""),
        registered_by=user,
    )
    # Auto-assign WORKSHOP_ADMIN role and membership to the registrant
    assign_role(user, UserRole.WORKSHOP_ADMIN)
    WorkshopMembership.objects.create(
        user=user,
        service_centre=centre,
        designation=Designation.ADMIN,
    )
    logger.info(f"ServiceCentre '{centre.name}' registered by {user.phone_number}")
    return centre


def get_verified_centres():
    return ServiceCentre.objects.filter(
        verification_status="VERIFIED", is_active=True
    ).order_by("name")


def get_all_centres():
    return ServiceCentre.objects.filter(is_active=True).order_by("name")


def get_centre_for_admin(centre_id: str, user: User) -> ServiceCentre:
    """Return centre only if the user is an active admin member."""
    try:
        membership = WorkshopMembership.objects.select_related("service_centre").get(
            user=user,
            service_centre_id=centre_id,
            is_active=True,
        )
        return membership.service_centre
    except WorkshopMembership.DoesNotExist:
        raise CentreNotFoundError("Service centre not found or access denied.")


def get_centre_for_member(centre_id: str, user: User) -> ServiceCentre:
    """Return centre if user has any active membership."""
    try:
        membership = WorkshopMembership.objects.select_related("service_centre").get(
            user=user,
            service_centre_id=centre_id,
            is_active=True,
        )
        return membership.service_centre
    except WorkshopMembership.DoesNotExist:
        raise CentreNotFoundError("Service centre not found or access denied.")


@transaction.atomic
def add_member(centre: ServiceCentre, admin: User, phone_number: str, designation: str) -> WorkshopMembership:
    """Add a user to the service centre."""
    phone_number = phone_number.strip().replace(" ", "").replace("-", "")
    try:
        target_user = User.objects.get(phone_number=phone_number, is_active=True)
    except User.DoesNotExist:
        raise MembershipError(
            f"No active VEDA account found for {phone_number}. "
            "The user must sign in to VEDA at least once before being added to a workshop."
        )

    if WorkshopMembership.objects.filter(user=target_user, service_centre=centre, is_active=True).exists():
        raise MembershipError(f"{phone_number} is already a member of this workshop.")

    # Assign appropriate role
    if designation == Designation.ADMIN:
        assign_role(target_user, UserRole.WORKSHOP_ADMIN)
    elif designation == Designation.MECHANIC:
        assign_role(target_user, UserRole.MECHANIC)

    membership = WorkshopMembership.objects.create(
        user=target_user,
        service_centre=centre,
        designation=designation,
    )
    logger.info(f"User {phone_number} added to '{centre.name}' as {designation}")
    return membership


def get_centre_members(centre: ServiceCentre):
    return WorkshopMembership.objects.filter(
        service_centre=centre, is_active=True
    ).select_related("user")


def get_user_centres(user: User):
    """Return all active centres a user belongs to."""
    return ServiceCentre.objects.filter(
        memberships__user=user,
        memberships__is_active=True,
        is_active=True,
    ).distinct()
