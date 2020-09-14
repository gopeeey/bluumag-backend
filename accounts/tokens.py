from django.contrib.auth.tokens import PasswordResetTokenGenerator
import six


class AccountVerificationTokenGenerator(PasswordResetTokenGenerator):

    def _make_hash_value(self, user, timestamp):
        return (
            six.text_type(user.pk) + six.text_type(timestamp) +
            six.text_type(user.verified)
        )


account_verification_token = AccountVerificationTokenGenerator()
