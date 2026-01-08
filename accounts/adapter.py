from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.core.exceptions import PermissionDenied


class BITSOnlySocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        email = sociallogin.user.email

        allowed_domains = [
            "pilani.bits-pilani.ac.in",
            "goa.bits-pilani.ac.in",
            "hyderabad.bits-pilani.ac.in",
        ]

        domain = email.split("@")[-1]

        if domain not in allowed_domains:
            raise PermissionDenied(
                "Only BITS email accounts are allowed to log in."
            )
