from enum import Enum


class Roles(str, Enum):
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'
