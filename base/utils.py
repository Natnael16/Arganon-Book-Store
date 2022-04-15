from django.contrib.auth.tokens import PasswordResetTokenGenerator
import six
class PasswordGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp: int) -> str:
        return six.text_type(user.is_active) + six.text_type(user.pk) + six.text_type(timestamp)

TokenGenerator = PasswordGenerator()