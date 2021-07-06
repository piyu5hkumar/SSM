# django imports
from django.contrib.auth.tokens import PasswordResetTokenGenerator


class ForgotPasswordTokenGenerator(PasswordResetTokenGenerator):
    '''
    We will call make_token of PasswordRestTokenGenerator,
    which uses _make_token_with_timestamp(self, user, timestamp, legacy=False),
    which further uses __make_hash_value(self, user, timestamp)
    So we are overriding __make_hash_value(self, user, timestamp)
    it is using the user.password salt and user.last_login timestamp.

    Both will change, and the link will no longer be valid.
    Also the self.secret(SECRET_KEY) is used in the salted_hmac function(inside _make_token_with_timestamp(self, user, timestamp, legacy=False)).
    So unless your SECRET_KEY was compromised, it would be impossible to reproduce the hash value.

    '''

    def _make_hash_value(self, user, timestamp):
        login_timestamp = (
            ''
            if user.last_login is None
            else user.last_login.replace(microsecond=0, tzinfo=None)
        )
        return f'{user.pk}{user.password}{login_timestamp}{timestamp}'
