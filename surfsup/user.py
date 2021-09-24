from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum, auto
from maps import Location


class AbilityLevel(Enum):
    PROFESSIONAL = auto()
    ADVANCED = auto()
    INTERMEDIATE = auto()
    BEGINNER = auto()


class BoardType(Enum):
    SHORTBOARD = auto()
    LOG = auto()
    FUN = auto()


class AccessLevel(Enum):
    FREE = auto()
    PAID = auto()
    HIKE = auto()
    LAUNCH_AREA = auto()


@dataclass
class UserPreferences:
    location: Location
    accessibility: AccessLevel


@dataclass
class UserSurfPreferences(UserPreferences):
    ability_score: int
    board_time: BoardType
    surf_height: int
    ability_level: AbilityLevel
    maximum_distance: int


class User:
    preferences: list[UserSurfPreferences]
    username: str

