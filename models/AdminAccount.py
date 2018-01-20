import hashlib
import random
import string

from google.appengine.ext import ndb

from config import app_config


class AdminAccount(ndb.Model):
    """Singleton class for admin account"""

    salt = ndb.StringProperty(required=True)
    hashed_password = ndb.StringProperty(required=True)
    hash_algorithm = ndb.StringProperty(required=True)
    last_modified = ndb.DateTimeProperty(auto_now=True)

    @classmethod
    def is_defined(cls):
        """:return whether singleton is created or not"""
        return cls.query().count() == 1

    @classmethod
    def get(cls):
        """:return the admin account in data store or a new one if it is not defined"""
        account = list(cls.query().fetch())
        if len(account) > 0:
            return account[0]
        else:
            account = AdminAccount()
            account.put()
            return account

    @staticmethod
    def create_salt():
        """:return random salt for password hashing"""
        s = string.ascii_letters + string.digits + string.punctuation
        length = app_config["default-login-salt-length"]
        return "".join([random.choice(s) for _ in xrange(length)])

    @staticmethod
    def calculate_password_strength(password):
        if not all(ord(char) < 128 for char in password):
            return -1

        score = len(password)
        password = set(password)
        char_classes = map(set, [string.lowercase, string.digits, string.uppercase, string.punctuation])

        for i in xrange(len(char_classes)):
            if len(password.intersection(char_classes[i])) > 0:
                score += i + 2

        return score

    def put(self, **kwargs):
        """
            Ensure that there's only one admin account in data store
        """
        if len(list(AdminAccount.query().fetch(keys_only=True))) > 0 and not self.key:
            raise SingletonError
        return super(AdminAccount, self)._put(**kwargs)

    def hash(self, password, salt=None, hash_algorithm=None):
        """
            Concat password and salt, then hash the result using the algorithm defined in config.py
            If no salt is provided, self.salt is used
        """
        if not salt:
            salt = self.salt
        if not hash_algorithm:
            hash_algorithm = getattr(hashlib, self.hash_algorithm)
        elif isinstance(hash_algorithm, str):
            hash_algorithm = getattr(hashlib, hash_algorithm)
        return hash_algorithm(password + salt).hexdigest()

    def validate_password(self, password):
        """Check if given password is correct"""
        return self.hashed_password == self.hash(password)

    def __init__(self, *args, **kwargs):
        # create new admin account if it does not exist
        if "salt" not in kwargs:
            salt = self.create_salt()
            kwargs["salt"] = salt
            hash_algorithm = app_config["hashing-algorithm"]
            kwargs["hash_algorithm"] = hash_algorithm

            hashed_password = self.hash(app_config["default-login-password"], salt, hash_algorithm)
            kwargs["hashed_password"] = hashed_password

        ndb.Model.__init__(self, *args, **kwargs)


class SingletonError(Exception):
    def __init__(self):
        self.message = "There can only be one entity of kind 'AdminAccount' in data store"
