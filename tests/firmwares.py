"""Functions to generate comments for different firmware versions."""
import datetime

from metamoth.config import (  # Config1_4_0,; Config1_5_0,; Config1_6_0,; Config1_7_0,; Config1_8_0,
    Config1_0,
    Config1_2_0,
    Config1_2_1,
    Config1_2_2,
)
from metamoth.enums import (  # ExtendedBatteryState,; FilterType,; GainSetting,
    BatteryState,
    RecordingState,
)

# from typing import Literal, Optional


def _get_datetime_1_0(time: datetime.datetime) -> str:
    return (
        f"{time.hour:02d}:{time.minute:02d}:{time.second:02d} "
        f"{time.day:02d}/{time.month:02d}/{time.year:04d}"
    )


def _get_gain_setting_1_0(gain: int) -> str:
    return f" at gain setting {gain}"


def _get_battery_state_1_0(battery_state: BatteryState) -> str:
    if battery_state == BatteryState.AM_BATTERY_LOW:
        return "while battery state was < 3.6V"

    if battery_state == BatteryState.AM_BATTERY_FULL:
        return "while battery state was > 5.0V"

    voltage = (battery_state.value + 35) / 10
    return f"while battery state was {voltage:1.2f}V"


def generate_comment_v1_0(
    time: datetime.datetime,
    serial_number: int,
    battery_state: BatteryState,
    config: Config1_0,
):
    """Generate a comment in the format of the firmware version 1.0."""

    time_str = _get_datetime_1_0(time)
    battery_str = _get_battery_state_1_0(battery_state)
    gain_str = _get_gain_setting_1_0(config.gain)

    return (
        f"Recorded at {time_str} by AudioMoth {serial_number:016x}"
        f"{gain_str} {battery_str}"
    )


def _get_battery_state_1_0_1(battery_state: BatteryState) -> str:
    if battery_state == BatteryState.AM_BATTERY_LOW:
        return "while battery state was < 3.6V"

    if battery_state == BatteryState.AM_BATTERY_FULL:
        return "while battery state was > 5.0V"

    voltage = (battery_state.value + 35) / 10
    return f"while battery state was {voltage:01.01f}V"


def generate_comment_v1_0_1(
    time: datetime.datetime,
    serial_number: int,
    battery_state: BatteryState,
    config: Config1_0,
):
    """Generate a comment in the format of the firmware version 1.0.1.

    Also used for firmware version 1.1.0.
    """
    time_str = _get_datetime_1_0(time)
    battery_str = _get_battery_state_1_0_1(battery_state)
    gain_str = _get_gain_setting_1_0(config.gain)
    timezone_str = "(UTC)"

    return (
        f"Recorded at {time_str} {timezone_str} by AudioMoth "
        f"{serial_number:016x}{gain_str} {battery_str}"
    )


def _get_timezone_1_2_0(timezone: int) -> str:
    if timezone == 0:
        return "(UTC)"

    if timezone > 0:
        return f"(UTC+{timezone:d})"

    return f"(UTC{timezone:d})"


def generate_comment_v1_2_0(
    time: datetime.datetime,
    serial_number: int,
    battery_state: BatteryState,
    config: Config1_2_0,
):
    """Generate a comment in the format of the firmware version 1.2.0."""
    time_str = _get_datetime_1_0(time)
    battery_str = _get_battery_state_1_0_1(battery_state)
    gain_str = _get_gain_setting_1_0(config.gain)
    timezone_str = _get_timezone_1_2_0(config.timezone)

    return (
        f"Recorded at {time_str} {timezone_str} by AudioMoth "
        f"{serial_number:016x}{gain_str} {battery_str}."
    )


def _get_battery_state_1_2_1(battery_state: BatteryState):
    if battery_state == BatteryState.AM_BATTERY_LOW:
        return "while battery state was less than 3.6V"

    if battery_state == BatteryState.AM_BATTERY_FULL:
        return "while battery state was greater than 4.9V"

    voltage = (battery_state.value + 35) / 10
    return f"while battery state was {voltage:01.01f}V"


def _get_state_1_2_1(recording_state: RecordingState):
    if recording_state == RecordingState.RECORDING_OKAY:
        return ""

    if recording_state == RecordingState.SUPPLY_VOLTAGE_LOW:
        return (
            " Recording cancelled before completion due to low battery voltage"
        )

    return " Recording cancelled before completion due to change of switch position"


def generate_comment_v1_2_1(
    time: datetime.datetime,
    serial_number: int,
    battery_state: BatteryState,
    config: Config1_2_1,
    recording_state: RecordingState,
):
    """Generate a comment in the format of the firmware version 1.2.1."""
    time_str = _get_datetime_1_0(time)
    battery_str = _get_battery_state_1_2_1(battery_state)
    gain_str = _get_gain_setting_1_0(config.gain)
    timezone_str = _get_timezone_1_2_0(config.timezone)
    state_str = _get_state_1_2_1(recording_state)

    return (
        f"Recorded at {time_str} {timezone_str} by AudioMoth "
        f"{serial_number:016x}{gain_str} {battery_str}.{state_str}"
    )


def _get_timezone_1_2_2(hours: int, minutes: int) -> str:
    if hours > 0:
        hours_str = f"+{hours:d}"
    elif hours < 0:
        hours_str = f"{hours:d}"
    else:
        hours_str = ""

    if minutes > 0:
        minutes_str = f":{minutes:2d}"
    elif minutes < 0:
        minutes_str = f":{-minutes:2d}"
    else:
        minutes_str = ""

    return f"(UTC{hours_str}{minutes_str})"



def generate_comment_v1_2_2(
    time: datetime.datetime,
    serial_number: int,
    battery_state: BatteryState,
    config: Config1_2_2,
    recording_state: RecordingState,
):
    """Generate a comment in the format of the firmware version 1.2.2."""

    time_str = _get_datetime_1_0(time)
    battery_str = _get_battery_state_1_2_1(battery_state)
    gain_str = _get_gain_setting_1_0(config.gain)
    timezone_str = _get_timezone_1_2_2(
        config.timezone_hours, config.timezone_minutes
    )
    state_str = _get_state_1_2_1(recording_state)

    return (
        f"Recorded at {time_str} {timezone_str} by AudioMoth "
        f"{serial_number:016x}{gain_str} {battery_str}.{state_str}"
    )

#
# def generate_comment_v1_4_0(
#     time: datetime.datetime,
#     serial_number: int,
#     extended_battery_state: ExtendedBatteryState,
#     config: Config1_4_0,
#     recording_state: RecordingState,
#     temperature: int,
# ):
#     """Generate a comment in the format of the firmware version 1.4.0.
#
#     Args:
#         time: The time the recording was made.
#         serial_number: The serial number of the AudioMoth.
#         gain: The gain setting used.
#         battery_state: The battery state at the time of recording.
#         timezone_hours: The timezone offset in hours.
#         timezone_minutes: The timezone offset in minutes.
#         battery_voltage_low: Whether the battery voltage was low.
#         switch_position_changed: Whether the switch position changed.
#         temperature: The temperature in degrees Celsius.
#         amplitude_threshold: The amplitude threshold.
#         filter_type: The filter type.
#         lower_filter_freq: The lower filter frequency.
#         higher_filter_freq: The higher filter frequency.
#
#
#     Returns:
#         The comment string.
#     """
#     if extended_battery_state == ExtendedBatteryState.AM_EXT_BAT_LOW:
#         battery = "less than 2.5V"
#     elif extended_battery_state == ExtendedBatteryState.AM_EXT_BAT_FULL:
#         battery = "greater than 4.9V"
#     else:
#         battery = f"{(extended_battery_state.value + 35) / 10:1.2f}V"
#
#     if timezone_hours > 0:
#         timezone_str = f"+{timezone_hours:d}"
#     elif timezone_hours < 0:
#         timezone_str = f"{timezone_hours:d}"
#     elif timezone_minutes < 0:
#         timezone_str = f"-{timezone_hours:d}"
#     elif timezone_minutes > 0:
#         timezone_str = f"+{timezone_hours:d}"
#     else:
#         timezone_str = ""
#
#     if timezone_minutes > 0:
#         timezone_str += f":{timezone_minutes:02d}"
#     elif timezone_minutes < 0:
#         timezone_str += f":{-timezone_minutes:02d}"
#
#     extra = ""
#     if battery_voltage_low or switch_position_changed:
#         cause = (
#             "low battery voltage"
#             if battery_voltage_low
#             else "switch position change"
#         )
#         extra = f" Recording cancelled before completion due to {cause}."
#
#     amplitude_str = ""
#     if amplitude_threshold > 0:
#         amplitude_str = f" Amplitude threshold was {amplitude_threshold:d}."
#
#     filter_str = ""
#     if filter_type == FilterType.LOW_PASS:
#         filter_str = (
#             f" Low-pass filter applied with cut-off frequency "
#             f"of {higher_filter_freq:01.01f}kHz."
#         )
#     elif filter_type == FilterType.HIGH_PASS:
#         filter_str = (
#             f" High-pass filter applied with cut-off frequency "
#             f"of {lower_filter_freq:01.01f}kHz."
#         )
#     elif filter_type == FilterType.BAND_PASS:
#         filter_str = (
#             f" Band-pass filter applied with cut-off frequencies of "
#             f"{lower_filter_freq:01.01f}kHz and {higher_filter_freq:01.01f}kHz."
#         )
#
#     gain_str = ["low", "low-medium", "medium", "medium-high", "high"][
#         gain.value
#     ]
#
#     return (
#         f"Recorded at {time.hour:02d}:{time.minute:02d}:{time.second:02d} "
#         f"{time.day:02d}/{time.month:02d}/{time.year:04d} "
#         f"(UTC{timezone_str}) by AudioMoth"
#         f"{serial_number:016x} at {gain_str} gain setting while battery "
#         f"state was {battery} and temperature was {temperature:1.2f}C."
#         f"{amplitude_str}{filter_str}{extra}"
#     )
#
#
# def generate_comment_v1_4_2(
#     time: datetime.datetime,
#     serial_number: int,
#     extended_battery_state: ExtendedBatteryState,
#     config: Config1_4_0,
#     recording_state: RecordingState,
#     temperature: int,
# ):
#     """Generate a comment in the format of the firmware version 1.4.2.
#
#     Args:
#         time: The time the recording was made.
#         serial_number: The serial number of the AudioMoth.
#         gain: The gain setting used.
#         battery_state: The battery state at the time of recording.
#         timezone_hours: The timezone offset in hours.
#         timezone_minutes: The timezone offset in minutes.
#         battery_voltage_low: Whether the battery voltage was low.
#         switch_position_changed: Whether the switch position changed.
#         temperature: The temperature in degrees Celsius.
#         amplitude_threshold: The amplitude threshold.
#         filter_type: The filter type.
#         lower_filter_freq: The lower filter frequency.
#         higher_filter_freq: The higher filter frequency.
#         file_size_limited: Whether the file size was limited.
#
#     Returns:
#         The comment string.
#     """
#     if extended_battery_state == ExtendedBatteryState.AM_EXT_BAT_LOW:
#         battery = "less than 2.5V"
#     elif extended_battery_state == ExtendedBatteryState.AM_EXT_BAT_FULL:
#         battery = "greater than 4.9V"
#     else:
#         battery = f"{(extended_battery_state.value + 35) / 10:1.2f}V"
#
#     if timezone_hours > 0:
#         timezone_str = f"+{timezone_hours:d}"
#     elif timezone_hours < 0:
#         timezone_str = f"{timezone_hours:d}"
#     elif timezone_minutes < 0:
#         timezone_str = f"-{timezone_hours:d}"
#     elif timezone_minutes > 0:
#         timezone_str = f"+{timezone_hours:d}"
#     else:
#         timezone_str = ""
#
#     if timezone_minutes > 0:
#         timezone_str += f":{timezone_minutes:02d}"
#     elif timezone_minutes < 0:
#         timezone_str += f":{-timezone_minutes:02d}"
#
#     gain_str = ["low", "low-medium", "medium", "medium-high", "high"][
#         gain.value
#     ]
#
#     extra = ""
#     if battery_voltage_low or switch_position_changed or file_size_limited:
#         if switch_position_changed:
#             cause = "change of switch position"
#         elif battery_voltage_low:
#             cause = "low voltage"
#         else:
#             cause = "file size limit"
#
#         extra = f" Recording cancelled before completion due to {cause}."
#
#     amplitude_str = ""
#     if amplitude_threshold > 0:
#         amplitude_str = f" Amplitude threshold was {amplitude_threshold:d}."
#
#     filter_str = ""
#     if filter_type == FilterType.LOW_PASS:
#         filter_str = (
#             f" Low-pass filter applied with cut-off frequency "
#             f"of {higher_filter_freq:01.01f}kHz."
#         )
#     elif filter_type == FilterType.HIGH_PASS:
#         filter_str = (
#             f" High-pass filter applied with cut-off frequency "
#             f"of {lower_filter_freq:01.01f}kHz."
#         )
#     elif filter_type == FilterType.BAND_PASS:
#         filter_str = (
#             f" Band-pass filter applied with cut-off frequencies of "
#             f"{lower_filter_freq:01.01f}kHz and {higher_filter_freq:01.01f}kHz."
#         )
#
#     return (
#         f"Recorded at {time.hour:02d}:{time.minute:02d}:{time.second:02d} "
#         f"{time.day:02d}/{time.month:02d}/{time.year:04d} "
#         f"(UTC{timezone_str}) by AudioMoth"
#         f"{serial_number:016x} at {gain_str} gain setting while battery "
#         f"state was {battery} and temperature was {temperature:1.2f}C."
#         f"{amplitude_str}{filter_str}{extra}"
#     )
#
#
# def generate_comment_v1_5_0(
#     time: datetime.datetime,
#     serial_number: int,
#     extended_battery_state: ExtendedBatteryState,
#     config: Config1_5_0,
#     recording_state: RecordingState,
#     temperature: int,
# ):
#     if timezone_hours > 0:
#         timezone_str = f"+{timezone_hours:d}"
#     elif timezone_hours < 0:
#         timezone_str = f"{timezone_hours:d}"
#     elif timezone_minutes < 0:
#         timezone_str = f"-{timezone_hours:d}"
#     elif timezone_minutes > 0:
#         timezone_str = f"+{timezone_hours:d}"
#     else:
#         timezone_str = ""
#
#     if timezone_minutes > 0:
#         timezone_str += f":{timezone_minutes:02d}"
#     elif timezone_minutes < 0:
#         timezone_str += f":{-timezone_minutes:02d}"
#
#     if deployment_id is not None:
#         deployment_str = f"during deployment {deployment_id:016x}"
#     else:
#         deployment_str = f"by AudioMoth {serial_number:016x}"
#
#     microphone_str = ""
#     if external_microphone:
#         microphone_str = " using external microphone"
#
#     gain_str = ["low", "low-medium", "medium", "medium-high", "high"][
#         gain.value
#     ]
#
#     if extended_battery_state == ExtendedBatteryState.AM_EXT_BAT_LOW:
#         battery = "less than 2.5V"
#     elif extended_battery_state == ExtendedBatteryState.AM_EXT_BAT_FULL:
#         battery = "greater than 4.9V"
#     else:
#         battery = f"{(extended_battery_state.value + 35) / 10:1.2f}V"
#
#     amplitude_str = ""
#     if amplitude_threshold > 0:
#         amplitude_str = f" Amplitude threshold was {amplitude_threshold:d}."
#
#     filter_str = ""
#     if filter_type == FilterType.LOW_PASS:
#         filter_str = (
#             f" Low-pass filter applied with cut-off frequency "
#             f"of {higher_filter_freq:01.01f}kHz."
#         )
#     elif filter_type == FilterType.HIGH_PASS:
#         filter_str = (
#             f" High-pass filter applied with cut-off frequency "
#             f"of {lower_filter_freq:01.01f}kHz."
#         )
#     elif filter_type == FilterType.BAND_PASS:
#         filter_str = (
#             f" Band-pass filter applied with cut-off frequencies of "
#             f"{lower_filter_freq:01.01f}kHz and {higher_filter_freq:01.01f}kHz."
#         )
#
#     extra = ""
#     if recording_state != RecordingState.RECORDING_OKAY:
#         cause = ""
#         if recording_state == RecordingState.MICROPHONE_CHANGED:
#             cause = "microphone change"
#         elif recording_state == RecordingState.SWITCH_CHANGED:
#             cause = "change of switch position"
#         elif recording_state == RecordingState.SUPPLY_VOLTAGE_LOW:
#             cause = "low voltage"
#         elif recording_state == RecordingState.FILE_SIZE_LIMITED:
#             cause = "file size limit"
#         extra = f" Recording cancelled before completion due to {cause}."
#
#     return (
#         f"Recorded at {time.hour:02d}:{time.minute:02d}:{time.second:02d} "
#         f"{time.day:02d}/{time.month:02d}/{time.year:04d} "
#         f"(UTC{timezone_str}) {deployment_str}{microphone_str}"
#         f" at {gain_str} gain setting while battery "
#         f"state was {battery} and temperature was {temperature:1.2f}C."
#         f"{amplitude_str}{filter_str}{extra}"
#     )
#
#
# def generate_comment_v1_6_0(
#     time: datetime.datetime,
#     serial_number: int,
#     extended_battery_state: ExtendedBatteryState,
#     config: Config1_6_0,
#     recording_state: RecordingState,
#     temperature: int,
# ):
#     if timezone_hours > 0:
#         timezone_str = f"+{timezone_hours:d}"
#     elif timezone_hours < 0:
#         timezone_str = f"{timezone_hours:d}"
#     elif timezone_minutes < 0:
#         timezone_str = f"-{timezone_hours:d}"
#     elif timezone_minutes > 0:
#         timezone_str = f"+{timezone_hours:d}"
#     else:
#         timezone_str = ""
#
#     if timezone_minutes > 0:
#         timezone_str += f":{timezone_minutes:02d}"
#     elif timezone_minutes < 0:
#         timezone_str += f":{-timezone_minutes:02d}"
#
#     if deployment_id is not None:
#         by_str = f"during deployment {deployment_id:016x}"
#     else:
#         by_str = f"by AudioMoth {serial_number:016x}"
#
#     microphone_str = " using external microphone" if external_microphone else ""
#
#     gain_str = ["low", "low-medium", "medium", "medium-high", "high"][
#         gain.value
#     ]
#
#     if extended_battery_state == ExtendedBatteryState.AM_EXT_BAT_LOW:
#         battery = "less than 2.5V"
#     elif extended_battery_state == ExtendedBatteryState.AM_EXT_BAT_FULL:
#         battery = "greater than 4.9V"
#     else:
#         battery = f"{(extended_battery_state.value + 35) / 10:01.01f}V"
#
#     amplitude_str = ""
#     if amplitude_threshold > 0:
#         if amplitude_threshold_format == "decibel":
#             threshold_str = f"-{amplitude_threshold:d} dB"
#         elif amplitude_threshold_format == "percentage":
#             threshold_str = f"{amplitude_threshold:d}%"
#         else:
#             threshold_str = f"{amplitude_threshold:d}"
#
#         amplitude_str = (
#             f" Amplitude threshold was {threshold_str} with "
#             f"{minimum_trigger_duration:d}s minimum trigger duration."
#         )
#
#     filter_str = ""
#     if filter_type == FilterType.LOW_PASS:
#         filter_str = (
#             f" Low-pass filter applied with cut-off frequency "
#             f"of {higher_filter_freq:01.01f}kHz."
#         )
#     elif filter_type == FilterType.HIGH_PASS:
#         filter_str = (
#             f" High-pass filter applied with cut-off frequency "
#             f"of {lower_filter_freq:01.01f}kHz."
#         )
#     elif filter_type == FilterType.BAND_PASS:
#         filter_str = (
#             f" Band-pass filter applied with cut-off frequencies of "
#             f"{lower_filter_freq:01.01f}kHz and {higher_filter_freq:01.01f}kHz."
#         )
#
#     state_str = ""
#     if recording_state != RecordingState.RECORDING_OKAY:
#         cause = ""
#         if recording_state == RecordingState.MICROPHONE_CHANGED:
#             cause = "microphone change"
#         elif recording_state == RecordingState.SWITCH_CHANGED:
#             cause = "change of switch position"
#         elif recording_state == RecordingState.SUPPLY_VOLTAGE_LOW:
#             cause = "low voltage"
#         elif recording_state == RecordingState.FILE_SIZE_LIMITED:
#             cause = "file size limit"
#         state_str = f" Recording stoped due to {cause}."
#
#     return (
#         f"Recorded at {time.hour:02d}:{time.minute:02d}:{time.second:02d} "
#         f"{time.day:02d}/{time.month:02d}/{time.year:04d} "
#         f"(UTC{timezone_str}) {by_str}{microphone_str}"
#         f" at {gain_str} gain setting while battery was {battery} and "
#         f"temperature was {temperature:1.1f}C.{amplitude_str}{filter_str}"
#         f"{state_str}."
#     )
#
#
# def generate_comment_v1_7_0(
#     time: datetime.datetime,
#     serial_number: int,
#     extended_battery_state: ExtendedBatteryState,
#     config: Config1_7_0,
#     recording_state: RecordingState,
#     temperature: int,
# ):
#     if timezone_hours > 0:
#         timezone_str = f"+{timezone_hours:d}"
#     elif timezone_hours < 0:
#         timezone_str = f"{timezone_hours:d}"
#     elif timezone_minutes < 0:
#         timezone_str = f"-{timezone_hours:d}"
#     elif timezone_minutes > 0:
#         timezone_str = f"+{timezone_hours:d}"
#     else:
#         timezone_str = ""
#
#     if timezone_minutes > 0:
#         timezone_str += f":{timezone_minutes:02d}"
#     elif timezone_minutes < 0:
#         timezone_str += f":{-timezone_minutes:02d}"
#
#     if deployment_id is not None:
#         by_str = f"during deployment {deployment_id:016x}"
#     else:
#         by_str = f"by AudioMoth {serial_number:016x}"
#
#     microphone_str = " using external microphone" if external_microphone else ""
#
#     gain_str = ["low", "low-medium", "medium", "medium-high", "high"][
#         gain.value
#     ]
#
#     if extended_battery_state == ExtendedBatteryState.AM_EXT_BAT_LOW:
#         battery = "less than 2.5V"
#     elif extended_battery_state == ExtendedBatteryState.AM_EXT_BAT_FULL:
#         battery = "greater than 4.9V"
#     else:
#         battery = f"{(extended_battery_state.value + 35) / 10:01.01f}V"
#
#     amplitude_str = ""
#     if amplitude_threshold > 0:
#         if amplitude_threshold_format == "decibel":
#             threshold_str = f"-{amplitude_threshold:d} dB"
#         elif amplitude_threshold_format == "percentage":
#             threshold_str = f"{amplitude_threshold:d}%"
#         else:
#             threshold_str = f"{amplitude_threshold:d}"
#
#         amplitude_str = (
#             f" Amplitude threshold was {threshold_str} with "
#             f"{minimum_trigger_duration:d}s minimum trigger duration."
#         )
#
#     filter_str = ""
#     if filter_type == FilterType.LOW_PASS:
#         filter_str = (
#             f" Low-pass filter applied with cut-off frequency "
#             f"of {higher_filter_freq:01.01f}kHz."
#         )
#     elif filter_type == FilterType.HIGH_PASS:
#         filter_str = (
#             f" High-pass filter applied with cut-off frequency "
#             f"of {lower_filter_freq:01.01f}kHz."
#         )
#     elif filter_type == FilterType.BAND_PASS:
#         filter_str = (
#             f" Band-pass filter applied with cut-off frequencies of "
#             f"{lower_filter_freq:01.01f}kHz and {higher_filter_freq:01.01f}kHz."
#         )
#
#     state_str = ""
#     if recording_state != RecordingState.RECORDING_OKAY:
#         cause = ""
#         if recording_state == RecordingState.MICROPHONE_CHANGED:
#             cause = "due to microphone change"
#         elif recording_state == RecordingState.SWITCH_CHANGED:
#             cause = "due to change of switch position"
#         elif recording_state == RecordingState.SUPPLY_VOLTAGE_LOW:
#             cause = "due to low voltage"
#         elif recording_state == RecordingState.FILE_SIZE_LIMITED:
#             cause = "due to file size limit"
#         elif recording_state == RecordingState.MAGNETIC_SWITCH:
#             cause = "by magnetic switch"
#         state_str = f" Recording stopped {cause}."
#
#     return (
#         f"Recorded at {time.hour:02d}:{time.minute:02d}:{time.second:02d} "
#         f"{time.day:02d}/{time.month:02d}/{time.year:04d} "
#         f"(UTC{timezone_str}) {by_str}{microphone_str}"
#         f" at {gain_str} gain setting while battery was {battery} and "
#         f"temperature was {temperature:1.1f}C.{amplitude_str}{filter_str}"
#         f"{state_str}."
#     )
#
#
# def generate_comment_v1_8_0(
#     time: datetime.datetime,
#     serial_number: int,
#     extended_battery_state: ExtendedBatteryState,
#     config: Config1_8_0,
#     recording_state: RecordingState,
#     temperature: int,
# ):
#     if timezone_hours > 0:
#         timezone_str = f"+{timezone_hours:d}"
#     elif timezone_hours < 0:
#         timezone_str = f"{timezone_hours:d}"
#     elif timezone_minutes < 0:
#         timezone_str = f"-{timezone_hours:d}"
#     elif timezone_minutes > 0:
#         timezone_str = f"+{timezone_hours:d}"
#     else:
#         timezone_str = ""
#
#     if timezone_minutes > 0:
#         timezone_str += f":{timezone_minutes:02d}"
#     elif timezone_minutes < 0:
#         timezone_str += f":{-timezone_minutes:02d}"
#
#     if deployment_id is not None:
#         by_str = f"during deployment {deployment_id:016x}"
#     else:
#         by_str = f"by AudioMoth {serial_number:016x}"
#
#     microphone_str = " using external microphone" if external_microphone else ""
#
#     gain_str = ["low", "low-medium", "medium", "medium-high", "high"][
#         gain.value
#     ]
#
#     if extended_battery_state == ExtendedBatteryState.AM_EXT_BAT_LOW:
#         battery = "less than 2.5V"
#     elif extended_battery_state == ExtendedBatteryState.AM_EXT_BAT_FULL:
#         battery = "greater than 4.9V"
#     else:
#         battery = f"{(extended_battery_state.value + 35) / 10:01.01f}V"
#
#     amplitude_str = ""
#     if amplitude_threshold > 0:
#         if amplitude_threshold_format == "decibel":
#             threshold_str = f"-{amplitude_threshold:d} dB"
#         elif amplitude_threshold_format == "percentage":
#             threshold_str = f"{amplitude_threshold:d}%"
#         else:
#             threshold_str = f"{amplitude_threshold:d}"
#
#         amplitude_str = (
#             f" Amplitude threshold was {threshold_str} with "
#             f"{minimum_trigger_duration:d}s minimum trigger duration."
#         )
#
#     frequency_str = ""
#     if frequency_trigger_enabled:
#         freq = frequency_trigger_centre_frequency / 1000
#         frequency_str = (
#             f" Frequency trigger ({freq:.2f}kHz and window length of "
#             f"{frequency_trigger_window_length_shift:d} samples)"
#             f" threshold was {frequency_trigger_threshold:.2f}% with "
#             f"{minimum_trigger_duration:d}s minimum trigger duration."
#         )
#
#     filter_str = ""
#     if filter_type == FilterType.LOW_PASS:
#         filter_str = (
#             f" Low-pass filter applied with cut-off frequency "
#             f"of {higher_filter_freq:01.01f}kHz."
#         )
#     elif filter_type == FilterType.HIGH_PASS:
#         filter_str = (
#             f" High-pass filter applied with cut-off frequency "
#             f"of {lower_filter_freq:01.01f}kHz."
#         )
#     elif filter_type == FilterType.BAND_PASS:
#         filter_str = (
#             f" Band-pass filter applied with cut-off frequencies of "
#             f"{lower_filter_freq:01.01f}kHz and {higher_filter_freq:01.01f}kHz."
#         )
#
#     state_str = ""
#     if recording_state != RecordingState.RECORDING_OKAY:
#         cause = ""
#         if recording_state == RecordingState.MICROPHONE_CHANGED:
#             cause = "due to microphone change"
#         elif recording_state == RecordingState.SWITCH_CHANGED:
#             cause = "due to change of switch position"
#         elif recording_state == RecordingState.SUPPLY_VOLTAGE_LOW:
#             cause = "due to low voltage"
#         elif recording_state == RecordingState.FILE_SIZE_LIMITED:
#             cause = "due to file size limit"
#         elif recording_state == RecordingState.MAGNETIC_SWITCH:
#             cause = "by magnetic switch"
#         state_str = f" Recording stopped {cause}."
#
#     return (
#         f"Recorded at {time.hour:02d}:{time.minute:02d}:{time.second:02d} "
#         f"{time.day:02d}/{time.month:02d}/{time.year:04d} "
#         f"(UTC{timezone_str}) {by_str}{microphone_str}"
#         f" at {gain_str} gain setting while battery was {battery} and "
#         f"temperature was {temperature:1.1f}C."
#         f"{frequency_str}{amplitude_str}{filter_str}"
#         f"{state_str}."
#     )
