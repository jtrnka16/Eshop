from django.contrib.auth.tokens import PasswordResetTokenGenerator


class UserVerificationTokenGenerator(PasswordResetTokenGenerator):
    """
    Custom token generator for user verification.
    Creates a unique hash value for the user based on their ID, timestamp, and active status.
    """

    def _make_hash_value(self, user, timestamp):
        """
        Generates a hash value for the user.

        Args:
            user: The user instance.
            timestamp: The timestamp when the token was generated.

        Returns:
            str: A unique hash value combining the user's ID, timestamp, and active status.
        """
        user_id = str(user.pk)
        ts = str(timestamp)
        is_active = str(user.is_active)
        return f"{user_id}{ts}{is_active}"


# Create an instance of the custom token generator
user_tokenizer_generate = UserVerificationTokenGenerator()
