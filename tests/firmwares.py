"""Functions to generate comments for different firmware versions."""
import datetime

from metamoth.enums import (
    BatteryState,
    ExtendedBatteryState,
    FilterType,
    GainSetting,
    RecordingState,
)


def generate_comment_v1_0(
    time: datetime.datetime,
    serial_number: int,
    gain: GainSetting,
    battery_state: BatteryState,
):
    """Generate a comment in the format of the firmware version 1.0."""

    if battery_state == BatteryState.BATTERY_LOW:
        battery = "< 3.6V"
    elif battery_state == BatteryState.BATTERY_FULL:
        battery = "> 5.0V"
    else:
        battery = f"{(battery_state.value + 35) / 10:1.2f}V"

    return (
        f"Recorded at {time.hour:02d}:{time.minute:02d}:{time.second:02d} "
        f"{time.day:02d}/{time.month:02d}/{time.year:04d} by AudioMoth "
        f"{serial_number:016x} at gain setting {gain.value} while battery "
        f"state was {battery}"
    )


def generate_comment_v1_0_1(
    time: datetime.datetime,
    serial_number: int,
    gain: GainSetting,
    battery_state: BatteryState,
):
    """Generate a comment in the format of the firmware version 1.0.1."""
    if battery_state == BatteryState.BATTERY_LOW:
        battery = "< 3.6V"
    elif battery_state == BatteryState.BATTERY_FULL:
        battery = "> 5.0V"
    else:
        battery = f"{(battery_state.value + 35) / 10:1.1f}V"

    return (
        f"Recorded at {time.hour:02d}:{time.minute:02d}:{time.second:02d} "
        f"{time.day:02d}/{time.month:02d}/{time.year:04d} (UTC) by AudioMoth "
        f"{serial_number:016x} at gain setting {gain.value} while battery "
        f"state was {battery}"
    )


def generate_comment_v1_2_0(
    time: datetime.datetime,
    serial_number: int,
    gain: GainSetting,
    battery_state: BatteryState,
    timezone: int,
):
    """Generate a comment in the format of the firmware version 1.2.0.

    Args:
        time: The time the recording was made.
        serial_number: The serial number of the AudioMoth.
        gain: The gain setting used.
        battery_state: The battery state at the time of recording.
        timezone: The timezone offset in hours.

    Returns:
        The comment string.
    """
    if battery_state == BatteryState.BATTERY_LOW:
        battery = "< 3.6V"
    elif battery_state == BatteryState.BATTERY_FULL:
        battery = "> 5.0V"
    else:
        battery = f"{(battery_state.value + 35) / 10:1.2f}V"

    if timezone > 0:
        timezone_str = f"+{timezone:d}"
    elif timezone < 0:
        timezone_str = f"{timezone:d}"
    else:
        timezone_str = ""

    return (
        f"Recorded at {time.hour:02d}:{time.minute:02d}:{time.second:02d} "
        f"{time.day:02d}/{time.month:02d}/{time.year:04d} "
        f"(UTC{timezone_str}) by AudioMoth "
        f"{serial_number:016x} at gain setting {gain.value} while battery "
        f"state was {battery}."
    )


def generate_comment_v1_2_1(
    time: datetime.datetime,
    serial_number: int,
    gain: GainSetting,
    battery_state: BatteryState,
    timezone: int,
    battery_voltage_low: bool,
    switch_position_changed: bool,
):
    """Generate a comment in the format of the firmware version 1.2.1.

    Args:
        time: The time the recording was made.
        serial_number: The serial number of the AudioMoth.
        gain: The gain setting used.
        battery_state: The battery state at the time of recording.
        timezone: The timezone offset in hours.
        battery_voltage_low: Whether the battery voltage was low.
        switch_position_changed: Whether the switch position changed.

    Returns:
        The comment string.
    """
    if battery_state == BatteryState.BATTERY_LOW:
        battery = "less than 3.6V"
    elif battery_state == BatteryState.BATTERY_FULL:
        battery = "greater than 4.9V"
    else:
        battery = f"{(battery_state.value + 35) / 10:1.2f}V"

    if timezone > 0:
        timezone_str = f"+{timezone:d}"
    elif timezone < 0:
        timezone_str = f"{timezone:d}"
    else:
        timezone_str = ""

    extra = ""
    if battery_voltage_low or switch_position_changed:
        cause = (
            "low battery voltage"
            if battery_voltage_low
            else "switch position change"
        )
        extra = f" Recording cancelled before completion due to {cause}"

    return (
        f"Recorded at {time.hour:02d}:{time.minute:02d}:{time.second:02d} "
        f"{time.day:02d}/{time.month:02d}/{time.year:04d} "
        f"(UTC{timezone_str}) by AudioMoth"
        f"{serial_number:016x} at gain setting {gain.value} while battery "
        f"state was {battery}.{extra}"
    )


def generate_comment_v1_2_2(
    time: datetime.datetime,
    serial_number: int,
    gain: GainSetting,
    battery_state: BatteryState,
    timezone_hours: int,
    timezone_minutes: int,
    battery_voltage_low: bool,
    switch_position_changed: bool,
):
    """Generate a comment in the format of the firmware version 1.2.2.

    Args:
        time: The time the recording was made.
        serial_number: The serial number of the AudioMoth.
        gain: The gain setting used.
        battery_state: The battery state at the time of recording.
        timezone_hours: The timezone offset in hours.
        timezone_minutes: The timezone offset in minutes.
        battery_voltage_low: Whether the battery voltage was low.
        switch_position_changed: Whether the switch position changed.

    Returns:
        The comment string.
    """
    if battery_state == BatteryState.BATTERY_LOW:
        battery = "less than 3.6V"
    elif battery_state == BatteryState.BATTERY_FULL:
        battery = "greater than 4.9V"
    else:
        battery = f"{(battery_state.value + 35) / 10:1.2f}V"

    if timezone_hours > 0:
        timezone_str = f"+{timezone_hours:d}"
    elif timezone_hours < 0:
        timezone_str = f"{timezone_hours:d}"
    else:
        timezone_str = ""

    if timezone_minutes > 0:
        timezone_str += f":{timezone_minutes:2d}"
    elif timezone_minutes < 0:
        timezone_str += f":{-timezone_minutes:2d}"

    extra = ""
    if battery_voltage_low or switch_position_changed:
        cause = (
            "low battery voltage"
            if battery_voltage_low
            else "switch position change"
        )
        extra = f" Recording cancelled before completion due to {cause}."

    return (
        f"Recorded at {time.hour:02d}:{time.minute:02d}:{time.second:02d} "
        f"{time.day:02d}/{time.month:02d}/{time.year:04d} "
        f"(UTC{timezone_str}) by AudioMoth"
        f"{serial_number:016x} at gain setting {gain.value} while battery "
        f"state was {battery}.{extra}"
    )


def generate_comment_v1_4_0(
    time: datetime.datetime,
    serial_number: int,
    gain: GainSetting,
    extended_battery_state: ExtendedBatteryState,
    timezone_hours: int,
    timezone_minutes: int,
    battery_voltage_low: bool,
    switch_position_changed: bool,
    temperature: int,
    amplitude_threshold: int,
    filter_type: FilterType,
    lower_filter_freq: int,
    higher_filter_freq: int,
):
    """Generate a comment in the format of the firmware version 1.4.0.

    Args:
        time: The time the recording was made.
        serial_number: The serial number of the AudioMoth.
        gain: The gain setting used.
        battery_state: The battery state at the time of recording.
        timezone_hours: The timezone offset in hours.
        timezone_minutes: The timezone offset in minutes.
        battery_voltage_low: Whether the battery voltage was low.
        switch_position_changed: Whether the switch position changed.
        temperature: The temperature in degrees Celsius.
        amplitude_threshold: The amplitude threshold.
        filter_type: The filter type.
        lower_filter_freq: The lower filter frequency.
        higher_filter_freq: The higher filter frequency.


    Returns:
        The comment string.
    """
    if extended_battery_state == ExtendedBatteryState.BATTERY_LOW:
        battery = "less than 2.5V"
    elif extended_battery_state == ExtendedBatteryState.BATTERY_FULL:
        battery = "greater than 4.9V"
    else:
        battery = f"{(extended_battery_state.value + 35) / 10:1.2f}V"

    if timezone_hours > 0:
        timezone_str = f"+{timezone_hours:d}"
    elif timezone_hours < 0:
        timezone_str = f"{timezone_hours:d}"
    elif timezone_minutes < 0:
        timezone_str = f"-{timezone_hours:d}"
    elif timezone_minutes > 0:
        timezone_str = f"+{timezone_hours:d}"
    else:
        timezone_str = ""

    if timezone_minutes > 0:
        timezone_str += f":{timezone_minutes:02d}"
    elif timezone_minutes < 0:
        timezone_str += f":{-timezone_minutes:02d}"

    extra = ""
    if battery_voltage_low or switch_position_changed:
        cause = (
            "low battery voltage"
            if battery_voltage_low
            else "switch position change"
        )
        extra = f" Recording cancelled before completion due to {cause}."

    amplitude_str = ""
    if amplitude_threshold > 0:
        amplitude_str = f" Amplitude threshold was {amplitude_threshold:d}."

    filter_str = ""
    if filter_type == FilterType.LOW_PASS:
        filter_str = (
            f" Low-pass filter applied with cut-off frequency "
            f"of {higher_filter_freq:01.01f}kHz."
        )
    elif filter_type == FilterType.HIGH_PASS:
        filter_str = (
            f" High-pass filter applied with cut-off frequency "
            f"of {lower_filter_freq:01.01f}kHz."
        )
    elif filter_type == FilterType.BAND_PASS:
        filter_str = (
            f" Band-pass filter applied with cut-off frequencies of "
            f"{lower_filter_freq:01.01f}kHz and {higher_filter_freq:01.01f}kHz."
        )

    gain_str = ["low", "low-medium", "medium", "medium-high", "high"][
        gain.value
    ]

    return (
        f"Recorded at {time.hour:02d}:{time.minute:02d}:{time.second:02d} "
        f"{time.day:02d}/{time.month:02d}/{time.year:04d} "
        f"(UTC{timezone_str}) by AudioMoth"
        f"{serial_number:016x} at {gain_str} gain setting while battery "
        f"state was {battery} and temperature was {temperature:1.2f}C."
        f"{amplitude_str}{filter_str}{extra}"
    )


def generate_comment_v1_4_2(
    time: datetime.datetime,
    serial_number: int,
    gain: GainSetting,
    extended_battery_state: ExtendedBatteryState,
    timezone_hours: int,
    timezone_minutes: int,
    battery_voltage_low: bool,
    switch_position_changed: bool,
    temperature: int,
    amplitude_threshold: int,
    filter_type: FilterType,
    lower_filter_freq: int,
    higher_filter_freq: int,
    file_size_limited: bool,
):
    """Generate a comment in the format of the firmware version 1.4.2.

    Args:
        time: The time the recording was made.
        serial_number: The serial number of the AudioMoth.
        gain: The gain setting used.
        battery_state: The battery state at the time of recording.
        timezone_hours: The timezone offset in hours.
        timezone_minutes: The timezone offset in minutes.
        battery_voltage_low: Whether the battery voltage was low.
        switch_position_changed: Whether the switch position changed.
        temperature: The temperature in degrees Celsius.
        amplitude_threshold: The amplitude threshold.
        filter_type: The filter type.
        lower_filter_freq: The lower filter frequency.
        higher_filter_freq: The higher filter frequency.
        file_size_limited: Whether the file size was limited.

    Returns:
        The comment string.
    """
    if extended_battery_state == ExtendedBatteryState.BATTERY_LOW:
        battery = "less than 2.5V"
    elif extended_battery_state == ExtendedBatteryState.BATTERY_FULL:
        battery = "greater than 4.9V"
    else:
        battery = f"{(extended_battery_state.value + 35) / 10:1.2f}V"

    if timezone_hours > 0:
        timezone_str = f"+{timezone_hours:d}"
    elif timezone_hours < 0:
        timezone_str = f"{timezone_hours:d}"
    elif timezone_minutes < 0:
        timezone_str = f"-{timezone_hours:d}"
    elif timezone_minutes > 0:
        timezone_str = f"+{timezone_hours:d}"
    else:
        timezone_str = ""

    if timezone_minutes > 0:
        timezone_str += f":{timezone_minutes:02d}"
    elif timezone_minutes < 0:
        timezone_str += f":{-timezone_minutes:02d}"

    gain_str = ["low", "low-medium", "medium", "medium-high", "high"][
        gain.value
    ]

    extra = ""
    if battery_voltage_low or switch_position_changed or file_size_limited:
        if switch_position_changed:
            cause = "change of switch position"
        elif battery_voltage_low:
            cause = "low voltage"
        else:
            cause = "file size limit"

        extra = f" Recording cancelled before completion due to {cause}."

    amplitude_str = ""
    if amplitude_threshold > 0:
        amplitude_str = f" Amplitude threshold was {amplitude_threshold:d}."

    filter_str = ""
    if filter_type == FilterType.LOW_PASS:
        filter_str = (
            f" Low-pass filter applied with cut-off frequency "
            f"of {higher_filter_freq:01.01f}kHz."
        )
    elif filter_type == FilterType.HIGH_PASS:
        filter_str = (
            f" High-pass filter applied with cut-off frequency "
            f"of {lower_filter_freq:01.01f}kHz."
        )
    elif filter_type == FilterType.BAND_PASS:
        filter_str = (
            f" Band-pass filter applied with cut-off frequencies of "
            f"{lower_filter_freq:01.01f}kHz and {higher_filter_freq:01.01f}kHz."
        )

    return (
        f"Recorded at {time.hour:02d}:{time.minute:02d}:{time.second:02d} "
        f"{time.day:02d}/{time.month:02d}/{time.year:04d} "
        f"(UTC{timezone_str}) by AudioMoth"
        f"{serial_number:016x} at {gain_str} gain setting while battery "
        f"state was {battery} and temperature was {temperature:1.2f}C."
        f"{amplitude_str}{filter_str}{extra}"
    )


def generate_comment_v1_5_0(
    time: datetime.datetime,
    serial_number: int,
    gain: GainSetting,
    extended_battery_state: ExtendedBatteryState,
    timezone_hours: int,
    timezone_minutes: int,
    temperature: int,
    amplitude_threshold: int,
    filter_type: FilterType,
    lower_filter_freq: int,
    higher_filter_freq: int,
    deployment_id: int,
    default_deployment_id: int,
    external_microphone: bool,
    recording_state: RecordingState,
):
    if timezone_hours > 0:
        timezone_str = f"+{timezone_hours:d}"
    elif timezone_hours < 0:
        timezone_str = f"{timezone_hours:d}"
    elif timezone_minutes < 0:
        timezone_str = f"-{timezone_hours:d}"
    elif timezone_minutes > 0:
        timezone_str = f"+{timezone_hours:d}"
    else:
        timezone_str = ""

    if timezone_minutes > 0:
        timezone_str += f":{timezone_minutes:02d}"
    elif timezone_minutes < 0:
        timezone_str += f":{-timezone_minutes:02d}"

    if deployment_id == default_deployment_id:
        deployment_str = "during deployment {deployment_id:016x}"
    else:
        deployment_str = "by AudioMoth {serial_number:016x}"

    microphone_str = ""
    if external_microphone:
        microphone_str = " using external microphone"

    gain_str = ["low", "low-medium", "medium", "medium-high", "high"][
        gain.value
    ]

    if extended_battery_state == ExtendedBatteryState.BATTERY_LOW:
        battery = "less than 2.5V"
    elif extended_battery_state == ExtendedBatteryState.BATTERY_FULL:
        battery = "greater than 4.9V"
    else:
        battery = f"{(extended_battery_state.value + 35) / 10:1.2f}V"

    amplitude_str = ""
    if amplitude_threshold > 0:
        amplitude_str = f" Amplitude threshold was {amplitude_threshold:d}."

    filter_str = ""
    if filter_type == FilterType.LOW_PASS:
        filter_str = (
            f" Low-pass filter applied with cut-off frequency "
            f"of {higher_filter_freq:01.01f}kHz."
        )
    elif filter_type == FilterType.HIGH_PASS:
        filter_str = (
            f" High-pass filter applied with cut-off frequency "
            f"of {lower_filter_freq:01.01f}kHz."
        )
    elif filter_type == FilterType.BAND_PASS:
        filter_str = (
            f" Band-pass filter applied with cut-off frequencies of "
            f"{lower_filter_freq:01.01f}kHz and {higher_filter_freq:01.01f}kHz."
        )

    extra = ""
    if recording_state != RecordingState.RECORDING_OKAY:
        cause = ""
        if recording_state == RecordingState.MICROPHONE_CHANGED:
            cause = "microphone change"
        elif recording_state == RecordingState.SWITCH_CHANGED:
            cause = "change of switch position"
        elif recording_state == RecordingState.VOLTAGE_CHECK:
            cause = "low voltage"
        elif recording_state == RecordingState.FILE_SIZE_LIMITED:
            cause = "file size limit"
        extra = f" Recording cancelled before completion due to {cause}."

    return (
        f"Recorded at {time.hour:02d}:{time.minute:02d}:{time.second:02d} "
        f"{time.day:02d}/{time.month:02d}/{time.year:04d} "
        f"(UTC{timezone_str}) {deployment_str}{microphone_str}"
        f" at {gain_str} gain setting while battery "
        f"state was {battery} and temperature was {temperature:1.2f}C."
        f"{amplitude_str}{filter_str}{extra}"
    )
