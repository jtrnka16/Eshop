from django.test import TestCase
from django.contrib.auth.models import User
from account.token import user_tokenizer_generate
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str


class UserVerificationTokenGeneratorTest(TestCase):

    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="password12345"
        )

    def test_token_generation(self):
        # Generate a token for the user
        token = user_tokenizer_generate.make_token(self.user)
        self.assertIsNotNone(token)  # Token should not be None

    def test_token_is_valid(self):
        # Generate a token and validate it
        token = user_tokenizer_generate.make_token(self.user)
        is_valid = user_tokenizer_generate.check_token(self.user, token)
        self.assertTrue(is_valid)  # Token should be valid

    def test_token_is_invalid_for_wrong_user(self):
        # Generate a token for one user
        token = user_tokenizer_generate.make_token(self.user)

        # Create another user
        another_user = User.objects.create_user(
            username="anotheruser",
            email="anotheruser@example.com",
            password="password67890"
        )

        # Validate the token for the other user
        is_valid = user_tokenizer_generate.check_token(another_user, token)
        self.assertFalse(is_valid)  # Token should be invalid for another user

    def test_token_is_invalid_if_user_is_deactivated(self):
        # Generate a token before deactivating the user
        token = user_tokenizer_generate.make_token(self.user)

        # Deactivate the user
        self.user.is_active = False
        self.user.save()

        # Refresh the user instance from the database
        self.user.refresh_from_db()

        # Validate the token for the deactivated user
        is_valid = user_tokenizer_generate.check_token(self.user, token)
        self.assertFalse(is_valid, "Token should be invalid for a deactivated user")

    def test_token_hash_includes_user_id_and_active_status(self):
        # Generate a hash value manually
        timestamp = 123456
        hash_value = user_tokenizer_generate._make_hash_value(self.user, timestamp)

        # Check if the hash value includes user ID and active status
        self.assertIn(str(self.user.pk), hash_value)
        self.assertIn(str(self.user.is_active), hash_value)
        self.assertIn(str(timestamp), hash_value)
