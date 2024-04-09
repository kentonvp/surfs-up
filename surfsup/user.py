from abc import ABC, abstractmethod
from dataclasses import dataclass
import traceback
from types import FunctionType
from typing import Optional
from enum import Enum, auto

import json

from surfsup.maps import Location


# class Parsable(ABC):
#     @staticmethod
#     @abstractmethod
#     def parse(s: str):
#         raise NotImplemented


class Activity(Enum):
    SHORTBOARD = auto()

    @staticmethod
    def parse(s: str):
        if s.lower() == "shortboard":
            return Activity.SHORTBOARD
        else:
            return Activity.SHORTBOARD


class AbilityLevel(Enum):
    PROFESSIONAL = auto()
    ADVANCED = auto()
    INTERMEDIATE = auto()
    BEGINNER = auto()

    @staticmethod
    def parse(s: str):
        if s.lower() == "professional":
            return AbilityLevel.PROFESSIONAL
        elif s.lower() == "advanced":
            return AbilityLevel.ADVANCED
        elif s.lower() == "intermediate":
            return AbilityLevel.INTERMEDIATE
        elif s.lower() == "beginner":
            return AbilityLevel.BEGINNER
        else:
            return AbilityLevel.INTERMEDIATE


class AccessLevel(Enum):
    FREE = auto()
    PAID = auto()
    HIKE = auto()
    LAUNCH_AREA = auto()
    ANY = auto()

    @staticmethod
    def parse(s: str):
        if s.lower() == "free":
            return AccessLevel.FREE
        elif s.lower() == "paid":
            return AccessLevel.PAID
        elif s.lower() == "hike":
            return AccessLevel.HIKE
        elif s.lower() == "launch_area":
            return AccessLevel.LAUNCH_AREA
        elif s.lower() == "any":
            return AccessLevel.ANY
        else:
            return AccessLevel.ANY


@dataclass
class ActivityPreferences:
    accessibility: AccessLevel = AccessLevel.ANY

    def to_dict(self):
        return {"accessibility": self.accessibility.name}


@dataclass
class ShortboardPreferences(ActivityPreferences):
    ability_score: AbilityLevel = AbilityLevel.INTERMEDIATE
    surf_height: int = 4
    travel_distance: int = 50

    @classmethod
    def de_json(cls, json_obj):
        return cls(
            AccessLevel.parse(json_obj["accessibility"]),
            AbilityLevel.parse(json_obj["ability"]),
            json_obj["surf_height"],
            json_obj["travel_distance"],
        )

    def __str__(self):
        return (
            f"Accessibility: {self.accessibility.name}\n"
            + f"Ability: {self.ability_score.name}\n"
            + f"Surf Height: {self.surf_height}\n"
            + f"Travel Distance: {self.travel_distance}"
        )

    def to_dict(self):
        return {
            "accessibility": "any",
            "ability": "intermediate",
            "surf_height": self.surf_height,
            "travel_distance": self.travel_distance,
        }

    def to_json(self):
        return json.dumps(self.to_dict)


def default_preferences(activity: Activity) -> ActivityPreferences:
    if activity == Activity.SHORTBOARD:
        return ShortboardPreferences()
    return ActivityPreferences()


def parse_activity_preferences(
    activity: Activity, json_obj: dict
) -> ActivityPreferences:
    if activity == Activity.SHORTBOARD:
        return ShortboardPreferences.de_json(json_obj)


class User:
    name: str
    # location: Optional[Location] = None
    activity: Activity
    preferences: dict[Activity, ActivityPreferences]

    def __init__(self, name, activity: Activity, preferences: dict = {}):
        self.name = name
        self.activity = activity
        self.preferences = preferences

    def get_activity_preferences(
        self, activity: Optional[Activity] = None
    ) -> ActivityPreferences:
        if activity is None:
            return self.preferences[self.activity]

        if activity in self.preferences:
            return self.preferences[activity]

        return default_preferences(activity)

    def add_activity_preferences(
        self, activity: Activity, activity_preferences: ActivityPreferences
    ) -> None:
        self.preferences[activity] = activity_preferences
        return None

    def set_activity(self, activity: Activity):
        self.activity = activity
        if activity not in self.preferences:
            self.preferences[activity] = default_preferences(activity)
        return None

    def current_activity(self):
        return self.activity

    @classmethod
    def de_json(cls, json_obj: dict):
        new_user = cls(
            json_obj["name"],
            Activity.parse(json_obj["activity"]),
            preferences={
                Activity.parse(k): parse_activity_preferences(Activity.parse(k), v)
                for (k, v) in json_obj["preferences"].items()
            },
        )

        return new_user

    def to_dict(self):
        return {
            "name": self.name,
            # 'location': self.location.to_dict(),
            "activity": self.activity.name,
            "preferences": {k.name: v.to_dict() for (k, v) in self.preferences.items()},
        }

    def to_json(self):
        return json.dumps(self.to_dict())

    def __str__(self):
        return self.to_json()

    def __eq__(self, other):
        if isinstance(other, User):
            return (
                self.name == other.name
                and self.activity == other.activity
                and len(self.preferences) == len(other.preferences)
            )
        return False


def export_users(fname: str, user_information: dict[int, User]):
    json_obj = {uid: user.to_dict() for (uid, user) in user_information.items()}
    with open(fname, "w+") as f:
        json.dump(json_obj, f)


def generate_user_information(json_obj: dict) -> dict[int, User]:
    user_information = {}
    try:
        if len(json_obj) == 0:
            return {}
        return {int(k): User.de_json(v) for (k, v) in json_obj.items()}
    except Exception as exc:
        trace = traceback.format_exc(limit=1)
        print(trace)
    return user_information


def read_users(fname: str) -> dict[int, User]:
    with open(fname, "r") as f:
        json_obj = json.load(f)

    return generate_user_information(json_obj)
