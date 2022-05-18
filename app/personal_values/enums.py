import typing
from enum import IntEnum, EnumMeta

DEFAULT_SEPARATOR = "_"


class KeyToNameEnumMeta(EnumMeta):
    def __getitem__(cls, name):
        """To make possible to initialize Enum not only with name,
        but also with a lowercase key like PersonalValue["self_direction"]"""
        try:
            name = name.upper()
        except AttributeError:
            pass
        return super().__getitem__(name)


class PersonalValue(IntEnum, metaclass=KeyToNameEnumMeta):
    """The order is equal to the ontology vector order,
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
        return self.separated_key(sep="-")

    def separated_key(self, sep: str = DEFAULT_SEPARATOR) -> str:
        return self.key.replace(DEFAULT_SEPARATOR, sep)

    @property
    def representation(self) -> str:
        """<PersonalValue.SELF_DIRECTION: 5> -> Self Direction"""
        return self.separated_key(sep=" ").title()

    @classmethod
    def get_all_keys(cls, sep: str = DEFAULT_SEPARATOR) -> typing.List[str]:
        return [v.separated_key(sep) for v in PersonalValue]
