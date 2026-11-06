"""
VEDA V2 — Auth unit tests

Covers:
- OTP code generation (6 digits, numeric, uses secrets)
- OTP hashing (SHA-256, raw code never stored)
- OTP verification (correct code passes, wrong fails, increments attempts)
- OTP expiry enforcement
- Attempt limiting
- Role assignment and detection
- JWT token issuance on successful verification
"""

import hashlib
import pytest
from django.utils import timezone
from datetime import timedelta

from apps.accounts.models import OTP, User, Role, UserRole
from apps.accounts import services


@pytest.mark.django_db
class TestOTPGeneration:
    def test_otp_is_six_digits(self):
        code = OTP.generate_code()
        assert code.isdigit()
        assert len(code) == 6

    def test_otp_in_valid_range(self):
        for _ in range(20):
            code = int(OTP.generate_code())
            assert 100000 <= code <= 999999

    def test_otp_hash_is_sha256(self):
        code = "123456"
        h = OTP.hash_code(code)
        assert h == hashlib.sha256(b"123456").hexdigest()
        assert len(h) == 64

    def test_raw_code_not_stored(self, db):
        user = User.objects.create(phone_number="+919999000001")
        result = services.request_otp("+919999000001")
        otp = OTP.objects.get(user=user)
        assert otp.code_hash != "123456"
        assert len(otp.code_hash) == 64  # SHA-256 hex

    def test_otp_expiry_set(self, db):
        User.objects.create(phone_number="+919999000002")
        services.request_otp("+919999000002")
        otp = OTP.objects.get(user__phone_number="+919999000002")
        assert otp.expires_at > timezone.now()

    def test_request_otp_invalidates_previous(self, db):
        User.objects.create(phone_number="+919999000003")
        services.request_otp("+919999000003")
        services.request_otp("+919999000003")
        active = OTP.objects.filter(
            user__phone_number="+919999000003", is_used=False
        ).count()
        assert active == 1  # Only one active at a time


@pytest.mark.django_db
class TestOTPVerification:
    def _create_otp(self, phone, raw_code="555555", expired=False, max_attempts=False):
        user, _ = User.objects.get_or_create(phone_number=phone)
        otp = OTP.objects.create(
            user=user,
            code_hash=OTP.hash_code(raw_code),
        )
        if expired:
            otp.expires_at = timezone.now() - timedelta(seconds=1)
            otp.save(update_fields=["expires_at"])
        if max_attempts:
            otp.attempt_count = 5
            otp.save(update_fields=["attempt_count"])
        return user, otp

    def test_correct_code_verifies(self, db):
        user, otp = self._create_otp("+919999001001", "111111")
        assert otp.verify("111111") is True
        assert otp.is_used is True

    def test_wrong_code_fails(self, db):
        user, otp = self._create_otp("+919999001002", "222222")
        assert otp.verify("999999") is False
        assert otp.is_used is False

    def test_wrong_code_increments_attempts(self, db):
        user, otp = self._create_otp("+919999001003", "333333")
        otp.verify("000000")
        otp.refresh_from_db()
        assert otp.attempt_count == 1

    def test_expired_otp_raises(self, db):
        user, otp = self._create_otp("+919999001004", "444444", expired=True)
        with pytest.raises(services.OTPExpiredError):
            services.verify_otp("+919999001004", "444444")

    def test_max_attempts_raises(self, db):
        user, otp = self._create_otp("+919999001005", "555555", max_attempts=True)
        with pytest.raises(services.OTPMaxAttemptsError):
            services.verify_otp("+919999001005", "555555")

    def test_wrong_code_raises_invalid(self, db):
        user, otp = self._create_otp("+919999001006", "666666")
        with pytest.raises(services.OTPInvalidError):
            services.verify_otp("+919999001006", "000000")

    def test_used_otp_not_reusable(self, db):
        user, otp = self._create_otp("+919999001007", "777777")
        otp.verify("777777")  # first verification
        with pytest.raises(services.AuthError):
            services.verify_otp("+919999001007", "777777")


@pytest.mark.django_db
class TestRoles:
    def test_assign_role(self, db):
        user = User.objects.create(phone_number="+919999002001")
        services.assign_role(user, UserRole.OWNER)
        assert user.has_role(UserRole.OWNER)

    def test_user_can_have_multiple_roles(self, db):
        user = User.objects.create(phone_number="+919999002002")
        services.assign_role(user, UserRole.OWNER)
        services.assign_role(user, UserRole.MECHANIC)
        roles = user.get_roles()
        assert UserRole.OWNER in roles
        assert UserRole.MECHANIC in roles

    def test_assign_role_idempotent(self, db):
        user = User.objects.create(phone_number="+919999002003")
        services.assign_role(user, UserRole.OWNER)
        services.assign_role(user, UserRole.OWNER)  # second time
        assert Role.objects.filter(user=user, role=UserRole.OWNER).count() == 1

    def test_remove_role(self, db):
        user = User.objects.create(phone_number="+919999002004")
        services.assign_role(user, UserRole.OWNER)
        services.remove_role(user, UserRole.OWNER)
        assert not user.has_role(UserRole.OWNER)

    def test_has_role_false_for_unassigned(self, db):
        user = User.objects.create(phone_number="+919999002005")
        assert not user.has_role(UserRole.VEDA_ADMIN)


@pytest.mark.django_db
class TestJWTIssuance:
    def test_verify_otp_returns_jwt_tokens(self, db):
        phone = "+919999003001"
        services.request_otp(phone)
        user = User.objects.get(phone_number=phone)
        otp = OTP.objects.filter(user=user, is_used=False).order_by("-created_at").first()
        # Find the raw code by brute-force (test-only approach)
        import secrets as sec
        for i in range(100000, 1000000):
            if OTP.hash_code(str(i)) == otp.code_hash:
                result = services.verify_otp(phone, str(i))
                assert "access" in result
                assert "refresh" in result
                assert result["user"]["phone_number"] == phone
                return
        pytest.fail("Could not find OTP code")
