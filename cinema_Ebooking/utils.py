from django.contrib.auth.tokens import PasswordResetTokenGenerator
import six


class TokenGenerator(PasswordResetTokenGenerator):

    def _make_hash_value(self, customuser, timestamp):
        return (six.text_type(customuser.email)+six.text_type(timestamp))

generate_token=TokenGenerator()