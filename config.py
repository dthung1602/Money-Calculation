#
#   Contains configurations for app
#

from google.appengine.api import app_identity

app_config = {
    "debug": True,
    "app-name": app_identity.get_application_id(),
    "default-login-password": "password",
    "default-login-salt-length": 25,
    "default-login-password-length": 25,
    "hashing-algorithm": "sha256",
    "person-name-max-length": 20
}
