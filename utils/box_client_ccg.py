"""
Handles the box client object creation
orchestrates the authentication process
"""

import os

from box_sdk_gen import BoxClient
from box_sdk_gen import BoxCCGAuth, CCGConfig


class ConfigCCG:
    """application configurations"""

    def __init__(self) -> None:
        # Common configurations
        self.client_id = os.getenv("CLIENT_ID")
        self.client_secret = os.getenv("CLIENT_SECRET")

        # CCG configurations
        self.enterprise_id = os.getenv("ENTERPRISE_ID")
        self.ccg_user_id = os.getenv("CCG_USER_ID")

        # Webhooks Keys
        self.key_a = os.getenv("KEY_A")
        self.key_b = os.getenv("KEY_B")


def __repr__(self) -> str:
    return f"ConfigCCG({self.__dict__})"


def get_ccg_enterprise_client(config: ConfigCCG) -> BoxClient:
    """Returns a box sdk Client object"""

    ccg = CCGConfig(
        client_id=config.client_id,
        client_secret=config.client_secret,
        enterprise_id=config.enterprise_id,
    )
    auth = BoxCCGAuth(ccg)

    client = BoxClient(auth)

    return client


def get_ccg_user_client(config: ConfigCCG, user_id: str) -> BoxClient:
    """Returns a box sdk Client object"""

    ccg = CCGConfig(
        client_id=config.client_id,
        client_secret=config.client_secret,
        user_id=user_id,
    )
    auth = BoxCCGAuth(ccg)
    # auth.as_user(user_id)

    client = BoxClient(auth)

    return client
