"""Enums for the AudioMoth configurations and state."""

from enum import Enum, auto

__all__ = [
    "GainSetting",
    "BatteryState",
    "ExtendedBatteryState",
    "RecordingState",
    "FilterType",
    "BatteryLevelDisplayType",
]


class GainSetting(Enum):
    """Gain setting."""

    AM_GAIN_LOW = 0
    AM_GAIN_LOW_MEDIUM = 1
    AM_GAIN_MEDIUM = 2
    AM_GAIN_MEDIUM_HIGH = 3
    AM_GAIN_HIGH = 4


class BatteryState(Enum):
    """Battery state."""

    AM_BATTERY_LOW = 0
    AM_BATTERY_3V6 = 1
    AM_BATTERY_3V7 = 2
    AM_BATTERY_3V8 = 3
    AM_BATTERY_3V9 = 4
    AM_BATTERY_4V0 = 5
    AM_BATTERY_4V1 = 6
    AM_BATTERY_4V2 = 7
    AM_BATTERY_4V3 = 8
    AM_BATTERY_4V4 = 9
    AM_BATTERY_4V5 = 10
    AM_BATTERY_4V6 = 11
    AM_BATTERY_4V7 = 12
    AM_BATTERY_4V8 = 13
    AM_BATTERY_4V9 = 14
    AM_BATTERY_FULL = 15

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

    AM_EXT_BAT_LOW = 0
    AM_EXT_BAT_2V5 = 1
    AM_EXT_BAT_2V6 = 2
    AM_EXT_BAT_2V7 = 3
    AM_EXT_BAT_2V8 = 4
    AM_EXT_BAT_2V9 = 5
    AM_EXT_BAT_3V0 = 6
    AM_EXT_BAT_3V1 = 7
    AM_EXT_BAT_3V2 = 8
    AM_EXT_BAT_3V3 = 9
    AM_EXT_BAT_3V4 = 10
    AM_EXT_BAT_3V5 = 11
    AM_EXT_BAT_3V6 = 12
    AM_EXT_BAT_3V7 = 13
    AM_EXT_BAT_3V8 = 14
    AM_EXT_BAT_3V9 = 15
    AM_EXT_BAT_4V0 = 16
    AM_EXT_BAT_4V1 = 17
    AM_EXT_BAT_4V2 = 18
    AM_EXT_BAT_4V3 = 19
    AM_EXT_BAT_4V4 = 20
    AM_EXT_BAT_4V5 = 21
    AM_EXT_BAT_4V6 = 22
    AM_EXT_BAT_4V7 = 23
    AM_EXT_BAT_4V8 = 24
    AM_EXT_BAT_4V9 = 25
    AM_EXT_BAT_FULL = 26

    @property
    def volts(self) -> float:
        """Return the battery voltage."""
        if self.value == 0:
            return 2.5
        if self.value == 26:
            return 5.0
        return (self.value + 24) / 10


class RecordingState(Enum):
    """Recording state."""

    RECORDING_OKAY = auto()
    FILE_SIZE_LIMITED = auto()
    SUPPLY_VOLTAGE_LOW = auto()
    SWITCH_CHANGED = auto()
    MICROPHONE_CHANGED = auto()
    MAGNETIC_SWITCH = auto()
    SDCARD_WRITE_ERROR = auto()


class FilterType(Enum):
    """Filter type."""

    NO_FILTER = auto()
    LOW_PASS = auto()
    BAND_PASS = auto()
    HIGH_PASS = auto()


class BatteryLevelDisplayType(Enum):
    """Battery level display type."""

    BATTERY_LEVEL = auto()
    NIMH_LIPO_BATTERY_VOLTAGE = auto()
