"""Database configuration.

No credentials live in the code. They come from, in order of preference:
  1. AWS Secrets Manager, when DB_SECRET_ARN is set (the AWS deployment: RDS-managed secret)
  2. Environment variables DB_USER and DB_PASSWORD (local development)

Other settings: DB_HOST (default localhost), DB_PORT (3306), DB_NAME (ecommerce),
DB_POOL_SIZE (5), AWS_REGION (ap-south-1, only used with Secrets Manager).
"""
import json
import os
from contextlib import contextmanager

from mysql.connector import pooling

_pool = None


def _load_credentials():
    secret_arn = os.environ.get("DB_SECRET_ARN")
    if secret_arn:
        import boto3

        client = boto3.client(
            "secretsmanager", region_name=os.environ.get("AWS_REGION", "ap-south-1")
        )
        secret = json.loads(client.get_secret_value(SecretId=secret_arn)["SecretString"])
        return secret["username"], secret["password"]

    try:
        return os.environ["DB_USER"], os.environ["DB_PASSWORD"]
    except KeyError as missing:
        raise RuntimeError(
            f"Database credentials not configured: set DB_SECRET_ARN, or DB_USER and DB_PASSWORD ({missing})"
        ) from None


def get_connection():
    """Return a connection from a shared pool (created on first use)."""
    global _pool
    if _pool is None:
        user, password = _load_credentials()
        _pool = pooling.MySQLConnectionPool(
            pool_name="ecommerce",
            pool_size=int(os.environ.get("DB_POOL_SIZE", "5")),
            host=os.environ.get("DB_HOST", "localhost"),
            port=int(os.environ.get("DB_PORT", "3306")),
            database=os.environ.get("DB_NAME", "ecommerce"),
            user=user,
            password=password,
        )
    return _pool.get_connection()


@contextmanager
def db_cursor():
    """One request = one connection = one transaction.

    Commits on success, rolls back on any error, and always returns the connection to the pool.
    """
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    try:
        yield cursor
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        cursor.close()
        connection.close()
