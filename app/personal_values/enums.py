from enum import IntEnum


class PersonalValue(IntEnum):
    CONFORMITY = 1
    TRADITION = 2
    BENEVOLENCE = 3
    UNIVERSALISM = 4
    SELF_DIRECTION = 5
    STIMULATION = 6
    HEDONISM = 7
    ACHIEVEMENT = 8
    POWER = 9
    SECURITY = 10

    @property
    def key(self):
        return self.name.lower()

    @property
    def dashed_key(self):
        return self.key.replace("_", "-")
