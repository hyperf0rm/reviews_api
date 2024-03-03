from enum import Enum


class Roles(str, Enum):
    """Class for defining user roles."""

    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'
