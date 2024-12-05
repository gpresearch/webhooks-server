from enum import Enum
import json
import re

import boto3
from botocore.exceptions import ClientError
from utils import logger

class RequiredSecrets(Enum):
    FORDEFI_ACCESS_TOKEN = "ACCESS_TOKEN"


class SecretsClient:
    """
    Client for retrieving secrets in the app.

    Can get secrets defined in RequiredSecrets enum.

    Is set up with a secrets_path which tells the client where to look for the secret
    in the underlying secrets store like AWS SecretsManager.

    e.g.

    secrets_client = SecretsClient("/path/to/my/secret")
    secrets_client.get_secret(RequiredSecrets.MY_SECRET)

    Will attempt to get secret at /path/to/my/secret/MY_SECRET:

        {
            "MY_SECRET": "my_secret_value"
        }

    will return "my_secret_value"
    """

    def __init__(self, secrets_path: str, aws_region: str):
        # breaking my own rule here of calling construcotr w/ in constructor
        # but i just want to make secrets manager easy for everyone to use.
        # forgive me.
        session = boto3.session.Session()
        self.client = session.client(
            service_name="secretsmanager",
            region_name=aws_region,
        )

        if not self._validate_secrets_path(secrets_path):
            raise ValueError(
                f"Secrets path {secrets_path} is invalid. Should be of type /<ENV>/<SERVICE>"
            )

        self.secrets_path = secrets_path

    def _validate_secrets_path(self, secrets_path: str):
        """
        Validate the secrets_path formatting.
        Should be of type /<ENV>/<SERVICE>

        Args:
            secrets_path (str): The path to the secret.

        Returns:
            bool: True if the path is valid, False otherwise.
        """
        pattern = r"^\/[^\/]+\/[^\/]+$"
        if re.match(pattern, secrets_path):
            return True
        return False

    def get_secret_path(self, secret: RequiredSecrets) -> str:
        """Get the path to the secret in our standard format"""
        return f"{self.secrets_path}/{secret.name}"

    def get_secret_json(self, secret: RequiredSecrets) -> dict[str, str | int | float]:
        """Get a json of secrets from AWS; return the json as a parsed dictionary"""
        full_secret_path = self.get_secret_path(secret=secret)
        secrets_dict = json.loads(
            self._get_json_secret_at_path(secret_path=full_secret_path)
        )
        return secrets_dict

    def get_secret(self, secret: RequiredSecrets) -> str:
        """
        Get the individual str secret from AWS Secrets Manager
        """
        secrets_dict = self.get_secret_json(secret=secret)
        return secrets_dict[secret.name]

    def _get_json_secret_at_path(self, secret_path: str):
        try:
            get_secret_value_response = self.client.get_secret_value(
                SecretId=secret_path
            )
        except ClientError as e:
            logger.info("Failed getting secret from AWS Secrets Manager: %s", e)
            # For a list of exceptions thrown, see
            # https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
            raise e
        except Exception as e:
            logger.info("Failed getting secret from AWS Secrets Manager: %s", e)
            raise e

        secret_json = get_secret_value_response["SecretString"]
        return secret_json
