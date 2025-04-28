"""
Handles user authentication using username/password pairs from the configuration.
Provides a dependency for protecting routes and identifying the current user.
"""

from fastapi import HTTPException, Header
from app.config import Config
from base64 import b64decode


USER_CREDENTIALS = {user["username"]: str(user["password"]) for user in Config.get("users")}

def authenticate_user(username: str, password: str) -> bool:
    """
    Validate the username and password against the configuration.
    Returns:
        bool: True if the credentials are valid, False otherwise.
    """

    return USER_CREDENTIALS.get(username) == password

def get_current_user(authorization: str = Header(None)) -> str:
    """
    Dependency to retrieve the currently authenticated user.
    Raises:
        HTTPException: If authentication fails.
    """
    if not authorization or not authorization.startswith("Basic "):
        raise HTTPException(status_code=401, detail="Authorization header missing or invalid")

    # Decode the Basic Auth credentials
    try:
        encoded_credentials = authorization.split(" ")[1]
        decoded_credentials = b64decode(encoded_credentials).decode("utf-8")
        username, password = decoded_credentials.split(":")
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid Authorization header format")

    # Validate the credentials
    if authenticate_user(username, password):
        return username

    raise HTTPException(status_code=401, detail="Invalid username or password")