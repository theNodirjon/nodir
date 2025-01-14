import email
import random

import redis
from django.core.mail import send_mail

from core import settings


class RedisDataStore:
    REDIS_HOST = 'localhost'
    REDIS_PORT = 6379
    DB = 0
    redis = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=DB, decode_responses=True)

    @classmethod
    def set_data(cls, key, value, expiration_seconds):
        """Store data in Redis with an expiration time.

        Args:
            key (str): The key to store the data under.
            value (str): The data to store.
            expiration_seconds (int): The time (in seconds) until the key expires.
        """
        cls.redis.setex(key, expiration_seconds, value)

    @classmethod
    def get_data(cls, key):
        """Retrieve data from Redis if it exists and is not expired.

        Args:
            key (str): The key to retrieve the data for.

        Returns:
            str or None: The data if it exists and has not expired; otherwise, None.
        """
        return cls.redis.get(key)

    @classmethod
    def is_expired(cls, key):
        """Check if a key is expired or does not exist.

        Args:
            key (str): The key to check.

        Returns:
            bool: True if the key is expired or does not exist; False otherwise.
        """
        ttl = cls.redis.ttl(key)
        return ttl == -2

    @classmethod
    def extend_expiration(cls, key, additional_seconds):
        """Extend the expiration time for a key.

        Args:
            key (str): The key to extend the expiration for.
            additional_seconds (int): Additional seconds to add to the current TTL.

        Returns:
            bool: True if the operation succeeded, False otherwise.
        """
        ttl = cls.redis.ttl(key)
        if ttl > 0:
            return cls.redis.expire(key, ttl + additional_seconds)
        return False

    @classmethod
    def delete_data(cls, key):
        """Delete a key from Redis.

        Args:
            key (str): The key to delete.

        Returns:
            int: The number of keys that were removed (0 or 1).
        """
        return cls.redis.delete(key)

    @classmethod
    def _send_v_email(cls, email_: str, code_: str):
        subject = 'Verification code'
        message = f'{code_}'

        # try:
        send_mail(subject, message, settings.EMAIL_HOST_USER, [email_])
        # context['result'] = 'Email sent successfully'
        # except Exception as e:
        #     print(e)
        #     pass
        # context['result'] = f'Error sending email: {e}'

    @classmethod
    def _send_verification_code(cls, email):
        code = str(random.randint(100000, 999999))
        cls._send_v_email(email, code)
        RedisDataStore.set_data(f'ev:{email}', code, 60)

    @classmethod
    def send_verification_code(cls, email):
        return cls._send_verification_code(email)
