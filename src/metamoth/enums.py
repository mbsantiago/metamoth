"""Enums for the AudioMoth configurations and state."""
from enum import Enum

__all__ = [
    "GainSetting",
    "BatteryState",
    "ExtendedBatteryState",
    "RecordingState",
    "FilterType",
]


class GainSetting(Enum):
    """Gain setting for the sensor."""

    LOW = 0
    LOW_MEDIUM = 1
    MEDIUM = 2
    MEDIUM_HIGH = 3
    HIGH = 4


class BatteryState(Enum):
    """Battery state."""

    BATTERY_LOW = 0
    BATTERY_3_6 = 1
    BATTERY_3_7 = 2
    BATTERY_3_8 = 3
    BATTERY_3_9 = 4
    BATTERY_4_0 = 5
    BATTERY_4_1 = 6
    BATTERY_4_2 = 7
    BATTERY_4_3 = 8
    BATTERY_4_4 = 9
    BATTERY_4_5 = 10
    BATTERY_4_6 = 11
    BATTERY_4_7 = 12
    BATTERY_4_8 = 13
    BATTERY_4_9 = 14
    BATTERY_FULL = 15

    @property
    def volts(self) -> float:
        """Return the battery voltage."""
        if self.value == 0:
            return 3.6
        if self.value == 15:
            return 5.0
        return (self.value + 35) / 10


class ExtendedBatteryState(Enum):
    """Extended battery state."""

    BATTERY_LOW = 0
    BATTERY_2_5 = 1
    BATTERY_2_6 = 2
    BATTERY_2_7 = 3
    BATTERY_2_8 = 4
    BATTERY_2_9 = 5
    BATTERY_3_0 = 6
    BATTERY_3_1 = 7
    BATTERY_3_2 = 8
    BATTERY_3_3 = 9
    BATTERY_3_4 = 10
    BATTERY_3_5 = 11
    BATTERY_3_6 = 12
    BATTERY_3_7 = 13
    BATTERY_3_8 = 14
    BATTERY_3_9 = 15
    BATTERY_4_0 = 16
    BATTERY_4_1 = 17
    BATTERY_4_2 = 18
    BATTERY_4_3 = 19
    BATTERY_4_4 = 20
    BATTERY_4_5 = 21
    BATTERY_4_6 = 22
    BATTERY_4_7 = 23
    BATTERY_4_8 = 24
    BATTERY_4_9 = 25
    BATTERY_FULL = 26


class RecordingState(Enum):
    """Recording state."""

    RECORDING_OKAY = 0
    SWITCH_CHANGED = 1
    SDCARD_WRITE_ERROR = 2
    VOLTAGE_CHECK = 3
    FILE_SIZE_LIMITED = 4
    SUPPLY_VOLTAGE_LOW = 5
    MICROPHONE_CHANGED = 6


class FilterType(Enum):
    """Filter type."""

    NO_FILTER = 0
    LOW_PASS = 1
    BAND_PASS = 2
    HIGH_PASS = 3
