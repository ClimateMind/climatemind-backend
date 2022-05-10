import typing
from enum import IntEnum


class PersonalValue(IntEnum):
    """The order is equal is ontology vector order,
    so it's safe to use list(PersonalValue)"""

    ACHIEVEMENT = 8
    BENEVOLENCE = 3
    CONFORMITY = 1
    HEDONISM = 7
    POWER = 9
    SECURITY = 10
    SELF_DIRECTION = 5
    STIMULATION = 6
    TRADITION = 2
    UNIVERSALISM = 4

    @property
    def key(self) -> str:
        return self.name.lower()

    @property
    def dashed_key(self) -> str:
        return self.key.replace("_", "-")

    @classmethod
    def get_all_keys(cls, dashed=False) -> typing.List[str]:
        if dashed:
            return [v.dashed_key for v in PersonalValue]
        else:
            return [v.key for v in PersonalValue]
