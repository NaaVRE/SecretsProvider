import os
from dotenv import get_key
from dotenv import set_key
from unittest import TestCase
from src.SecretsProvider import SecretsProvider

class TestSecretsProvider(TestCase):
    def tearDown(self):
        if os.path.exists(SecretsProvider.env_path):
            os.remove(SecretsProvider.env_path)

    def test_set_secret_new_secret(self):
        secret1_name: str = "secret1"
        secret1_value: str = "secret1_value"
        mock_input = lambda prompt: secret1_value

        SecretsProvider(input_func=mock_input).set_secret(secret1_name)

        self.assertEqual(secret1_value, get_key(SecretsProvider.env_path, secret1_name))

    def test_set_secret_no_input(self):
        secret1_name: str = "secret1"
        mock_input = lambda prompt: ""

        SecretsProvider(input_func=mock_input).set_secret(secret1_name)

        self.assertIsNone(get_key(SecretsProvider.env_path, secret1_name))

    def test_set_secret_space_input(self):
        secret1_name: str = "secret1"
        mock_input = lambda prompt: " "

        SecretsProvider(input_func=mock_input).set_secret(secret1_name)

        self.assertIsNone(get_key(SecretsProvider.env_path, secret1_name))

    def test_set_secret_overwrite(self):
        secret1_name: str = "secret1"
        secret1_original_value: str = "secret1_original_value"
        secret1_new_value: str = "secret1_new_value"
        set_key(SecretsProvider.env_path, secret1_name, secret1_original_value)
        mock_input = lambda prompt: secret1_new_value

        SecretsProvider(input_func=mock_input).set_secret(secret1_name)

        self.assertEqual(secret1_new_value, get_key(SecretsProvider.env_path, secret1_name))

    def test_get_secret_nonexistent(self):
        secret1_name: str = "secret1"
        secret1_value: str = "secret1_value"
        mock_input = lambda prompt: secret1_value

        secret_value = SecretsProvider(input_func=mock_input).get_secret(secret1_name)

        self.assertEqual(secret1_value, get_key(SecretsProvider.env_path, secret1_name), secret_value)

    def test_get_secret_existent(self):
        secret1_name: str = "secret1"
        secret1_value: str = "secret1_value"
        set_key(SecretsProvider.env_path, secret1_name, secret1_value)

        self.assertEqual(secret1_value, SecretsProvider().get_secret(secret1_name))

    def test_print_secrets(self):
        secret1_name: str = "secret1"
        secret1_value: str = "secret1_value"
        secret2_name: str = "secret2"
        secret2_value: str = "secret2_value"
        set_key(SecretsProvider.env_path, secret1_name, secret1_value)
        set_key(SecretsProvider.env_path, secret2_name, secret2_value)

        SecretsProvider().print_secrets()

    def test_print_secrets_no_secrets_stored(self):
        SecretsProvider().print_secrets()

    def test_remove_secret(self):
        secret1_name: str = "secret1"
        secret1_value: str = "secret1_value"
        set_key(SecretsProvider.env_path, secret1_name, secret1_value)

        SecretsProvider().remove_secret(secret1_name)

        self.assertIsNone(get_key(SecretsProvider.env_path, secret1_name))