"""Functions to generate comments for different firmware versions."""

# pylint: disable=too-many-arguments,too-many-locals
import datetime
from typing import Optional

from metamoth.config import (
    Config1_0,
    Config1_2_0,
    Config1_2_1,
    Config1_2_2,
    Config1_4_0,
    Config1_5_0,
    Config1_6_0,
    Config1_7_0,
    Config1_8_0,
)
from metamoth.enums import (
    BatteryState,
    ExtendedBatteryState,
    GainSetting,
    RecordingState,
)


def _get_datetime_1_0(time: datetime.datetime) -> str:
    return (
        f"{time.hour:02d}:{time.minute:02d}:{time.second:02d} "
        f"{time.day:02d}/{time.month:02d}/{time.year:04d}"
    )


def _get_gain_setting_1_0(gain: int) -> str:
    return f"gain setting {gain}"


def _get_battery_state_1_0(battery_state: BatteryState) -> str:
    """Get the battery state as a string for firmware version 1.0."""
    if battery_state == BatteryState.AM_BATTERY_LOW:
        return "battery state was < 3.6V"

    if battery_state == BatteryState.AM_BATTERY_FULL:
        return "battery state was > 5.0V"

    voltage = (battery_state.value + 35) / 10
    return f"battery state was {voltage:1.2f}V"


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
        f"Recorded at {time_str} by AudioMoth {serial_number:016x} "
        f"at {gain_str} while {battery_str}"
    )


def _get_battery_state_1_0_1(battery_state: BatteryState) -> str:
    if battery_state == BatteryState.AM_BATTERY_LOW:
        return "battery state was < 3.6V"

    if battery_state == BatteryState.AM_BATTERY_FULL:
        return "battery state was > 5.0V"

    voltage = (battery_state.value + 35) / 10
    return f"battery state was {voltage:01.01f}V"


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
        f"{serial_number:016x} at {gain_str} while {battery_str}"
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
        f"{serial_number:016x} at {gain_str} while {battery_str}."
    )


def _get_battery_state_1_2_1(battery_state: BatteryState):
    if battery_state == BatteryState.AM_BATTERY_LOW:
        return "battery state was less than 3.6V"

    if battery_state == BatteryState.AM_BATTERY_FULL:
        return "battery state was greater than 4.9V"

    voltage = (battery_state.value + 35) / 10
    return f"battery state was {voltage:01.01f}V"


def _get_recording_state_1_2_1(recording_state: RecordingState):
    if recording_state == RecordingState.RECORDING_OKAY:
        return ""

    cause = "change of switch position"

    if recording_state == RecordingState.SUPPLY_VOLTAGE_LOW:
        cause = "low battery voltage"

    return f" Recording cancelled before completion due to {cause}."


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
    recording_state_str = _get_recording_state_1_2_1(recording_state)

    return (
        f"Recorded at {time_str} {timezone_str} by AudioMoth "
        f"{serial_number:016x} at {gain_str} while {battery_str}."
        f"{recording_state_str}"
    )


def _get_timezone_1_2_2(hours: int, minutes: int) -> str:
    if hours > 0:
        hours_str = f"+{hours:d}"
    elif hours < 0:
        hours_str = f"{hours:d}"
    elif minutes != 0:
        hours_str = "+0"
    else:
        hours_str = ""

    if minutes > 0:
        minutes_str = f":{minutes:02d}"
    elif minutes < 0:
        minutes_str = f":{-minutes:02d}"
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
    """Generate a comment in the format of the firmware version 1.2.2.

    Also used for firmware version 1.3.0.
    """
    time_str = _get_datetime_1_0(time)
    battery_str = _get_battery_state_1_2_1(battery_state)
    gain_str = _get_gain_setting_1_0(config.gain)
    timezone_str = _get_timezone_1_2_2(
        config.timezone_hours, config.timezone_minutes
    )
    recording_state_str = _get_recording_state_1_2_1(recording_state)

    return (
        f"Recorded at {time_str} {timezone_str} by AudioMoth "
        f"{serial_number:016x} at {gain_str} while {battery_str}."
        f"{recording_state_str}"
    )


def _get_frequency_filter_1_4_0(
    lower_filter_freq: int, higher_filter_freq: int
) -> str:
    """Get the frequency filter string.

    We assume that the filter frequencies are in units of Hz.
    """
    if lower_filter_freq == 0 and higher_filter_freq == 0:
        return ""

    low_freq = lower_filter_freq / 1000
    high_freq = higher_filter_freq / 1000

    if lower_filter_freq > 0 and higher_filter_freq > 0:
        return (
            " Band-pass filter applied with cut-off frequencies of "
            f"{low_freq:01.01f}kHz and {high_freq:01.01f}kHz."
        )

    if higher_filter_freq > 0:
        return (
            " Low-pass filter applied with cut-off frequency of "
            f"{high_freq:01.01f}kHz."
        )

    return (
        " High-pass filter applied with cut-off frequency of "
        f"{low_freq:01.01f}kHz."
    )


def _get_temperature_1_4_0(temperature: float) -> str:
    return f"temperature was {temperature:2.1f}C"


def _get_battery_state_1_4_0(battery_state: ExtendedBatteryState) -> str:
    if battery_state == ExtendedBatteryState.AM_EXT_BAT_LOW:
        return "battery state was less than 2.5V"

    if battery_state == ExtendedBatteryState.AM_EXT_BAT_FULL:
        return "battery state was greater than 4.9V"

    voltage = battery_state.volts
    return f"battery state was {voltage:01.01f}V"


def _get_gain_setting_1_4_0(gain: int) -> str:
    gain_str = ["low", "low-medium", "medium", "medium-high", "high"][gain]
    return f"{gain_str} gain setting"


def _get_timezone_1_4_0(hours: int, minutes: int) -> str:
    hours_str = ""
    if hours > 0:
        hours_str = f"+{hours:d}"
    elif hours < 0:
        hours_str = f"{hours:d}"

    minutes_str = ""
    if minutes < 0:
        if hours == 0:
            hours_str = "-0"
        minutes_str = f":{-minutes:d}"
    elif minutes > 0:
        if hours == 0:
            hours_str = "+0"
        minutes_str = f":{minutes:02d}"

    return f"(UTC{hours_str}{minutes_str})"


def _get_amplitude_threshold_1_4_0(amplitude_threshold: int) -> str:
    if amplitude_threshold == 0:
        return ""

    return f" Amplitude threshold was {amplitude_threshold:d}."


def _get_recording_state_1_4_0(recording_state: RecordingState) -> str:
    if recording_state == RecordingState.RECORDING_OKAY:
        return ""

    template = " Recording cancelled before completion due to {cause}."

    if recording_state == RecordingState.SUPPLY_VOLTAGE_LOW:
        return template.format(cause="low voltage")

    if recording_state == RecordingState.SWITCH_CHANGED:
        return template.format(cause="change of switch position")

    return ""


def generate_comment_v1_4_0(
    time: datetime.datetime,
    serial_number: int,
    extended_battery_state: ExtendedBatteryState,
    config: Config1_4_0,
    recording_state: RecordingState,
    temperature: float,
):
    """Generate a comment in the format of the firmware version 1.4.0.

    Also valid for version 1.4.1.
    """
    time_str = _get_datetime_1_0(time)
    battery_str = _get_battery_state_1_4_0(extended_battery_state)
    gain_str = _get_gain_setting_1_4_0(config.gain)
    timezone_str = _get_timezone_1_4_0(
        config.timezone_hours,
        config.timezone_minutes,
    )
    recording_state_str = _get_recording_state_1_4_0(recording_state)
    filter_str = _get_frequency_filter_1_4_0(
        config.lower_filter_freq,
        config.higher_filter_freq,
    )
    temperature_str = _get_temperature_1_4_0(temperature)
    amplitude_threshold_str = _get_amplitude_threshold_1_4_0(
        config.amplitude_threshold
    )

    return (
        f"Recorded at {time_str} {timezone_str} by AudioMoth "
        f"{serial_number:016x} at {gain_str} while {battery_str} "
        f"and {temperature_str}.{amplitude_threshold_str}"
        f"{filter_str}{recording_state_str}"
    )


def _get_recording_state_1_4_2(recording_state: RecordingState) -> str:
    if recording_state == RecordingState.RECORDING_OKAY:
        return ""

    cause = "change of switch position"

    if recording_state == RecordingState.SUPPLY_VOLTAGE_LOW:
        cause = "low voltage"

    if recording_state == RecordingState.FILE_SIZE_LIMITED:
        cause = "file size limit"

    return f" Recording cancelled before completion due to {cause}."


def generate_comment_v1_4_2(
    time: datetime.datetime,
    serial_number: int,
    extended_battery_state: ExtendedBatteryState,
    config: Config1_4_0,
    recording_state: RecordingState,
    temperature: float,
):
    """Generate a comment in the format of the firmware version 1.4.2.

    Also valid for versions 1.4.3 and 1.4.4.
    """
    time_str = _get_datetime_1_0(time)
    battery_str = _get_battery_state_1_4_0(extended_battery_state)
    gain_str = _get_gain_setting_1_4_0(config.gain)
    timezone_str = _get_timezone_1_4_0(
        config.timezone_hours,
        config.timezone_minutes,
    )
    recording_state_str = _get_recording_state_1_4_2(recording_state)
    filter_str = _get_frequency_filter_1_4_0(
        config.lower_filter_freq,
        config.higher_filter_freq,
    )
    temperature_str = _get_temperature_1_4_0(temperature)
    amplitude_threshold_str = _get_amplitude_threshold_1_4_0(
        config.amplitude_threshold
    )

    return (
        f"Recorded at {time_str} {timezone_str} by AudioMoth "
        f"{serial_number:016x} at {gain_str} while {battery_str} "
        f"and {temperature_str}.{amplitude_threshold_str}"
        f"{filter_str}{recording_state_str}"
    )


def _get_artist_1_5_0(serial_number: int, deployment_id: Optional[int]) -> str:
    if deployment_id is None:
        return f"by AudioMoth {serial_number:016x}"

    return f"during deployment {deployment_id:016x}"


def _get_microphone_1_5_0(external_microphone: bool) -> str:
    if not external_microphone:
        return ""

    return "using external microphone "


def _get_recording_state_1_5_0(recording_state: RecordingState) -> str:
    if recording_state == RecordingState.RECORDING_OKAY:
        return ""

    cause = "change of switch position"

    if recording_state == RecordingState.MICROPHONE_CHANGED:
        cause = "microphone change"

    if recording_state == RecordingState.SUPPLY_VOLTAGE_LOW:
        cause = "low voltage"

    if recording_state == RecordingState.FILE_SIZE_LIMITED:
        cause = "file size limit"

    return f" Recording cancelled before completion due to {cause}."


def generate_comment_v1_5_0(
    time: datetime.datetime,
    serial_number: int,
    extended_battery_state: ExtendedBatteryState,
    config: Config1_5_0,
    recording_state: RecordingState,
    temperature: float,
    deployment_id: Optional[int],
    external_microphone: bool,
):
    """Generate a comment in the format of the firmware version 1.5.0."""
    time_str = _get_datetime_1_0(time)
    timezone_str = _get_timezone_1_4_0(
        config.timezone_hours,
        config.timezone_minutes,
    )
    microphone_str = _get_microphone_1_5_0(external_microphone)
    artist_str = _get_artist_1_5_0(serial_number, deployment_id)
    gain_str = _get_gain_setting_1_4_0(config.gain)
    battery_str = _get_battery_state_1_4_0(extended_battery_state)
    temperature_str = _get_temperature_1_4_0(temperature)
    filter_str = _get_frequency_filter_1_4_0(
        config.lower_filter_freq,
        config.higher_filter_freq,
    )
    amplitude_threshold_str = _get_amplitude_threshold_1_4_0(
        config.amplitude_threshold
    )
    recording_state_str = _get_recording_state_1_5_0(recording_state)

    return (
        f"Recorded at {time_str} {timezone_str} {artist_str} {microphone_str}"
        f"at {gain_str} while {battery_str} "
        f"and {temperature_str}.{amplitude_threshold_str}"
        f"{filter_str}{recording_state_str}"
    )


def _get_gain_setting_1_6_0(gain: int) -> str:
    gain_str = ["low", "low-medium", "medium", "medium-high", "high"][gain]
    return f"{gain_str} gain"


def _format_decibels(decibels: int) -> str:
    if decibels == 0:
        return "0 dB"

    return f"-{decibels:d} dB"


def _format_percentage(mantissa: int, exponent: int) -> str:
    """Convert a mantissa and exponent to a percentage.

    An almost verbatim copy of the formatPercentage in the source code.

    This function should take an integer mantissa and an exponent and
    return the decimal representation.

    However this implementation only works if the mantissa is a single
    digit number!
    """
    length = 1 - exponent if exponent < 0 else 0
    perc = "0.0000"[:length]
    perc += f"{mantissa:d}"
    if exponent > 0:
        perc += "0" * exponent
    perc += "%"
    return perc


def _get_amplitude_threshold_1_6_0(
    amplitude_threshold: int,
    enable_amplitude_threshold_decibel_scale: bool,
    enable_amplitude_threshold_percentage_scale: bool,
    minimum_trigger_duration: int,
    amplitude_threshold_decibels: int,
    amplitude_threshold_percentage_mantissa: int,
    amplitude_threshold_percentage_exponent: int,
) -> str:
    if (
        amplitude_threshold == 0
        and not enable_amplitude_threshold_decibel_scale
        and not enable_amplitude_threshold_percentage_scale
    ):
        return ""

    threshold_str = f"{amplitude_threshold:d}"

    if (
        enable_amplitude_threshold_decibel_scale
        and not enable_amplitude_threshold_percentage_scale
    ):
        threshold_str = _format_decibels(amplitude_threshold_decibels)

    if (
        not enable_amplitude_threshold_decibel_scale
        and enable_amplitude_threshold_percentage_scale
    ):
        threshold_str = _format_percentage(
            amplitude_threshold_percentage_mantissa,
            amplitude_threshold_percentage_exponent,
        )

    return (
        f" Amplitude threshold was {threshold_str} with "
        f"{minimum_trigger_duration:d}s minimum trigger duration."
    )


def _get_recording_state_1_6_0(recording_state: RecordingState) -> str:
    if recording_state == RecordingState.RECORDING_OKAY:
        return ""

    cause = "switch position change"

    if recording_state == RecordingState.MICROPHONE_CHANGED:
        cause = "microphone change"

    if recording_state == RecordingState.SUPPLY_VOLTAGE_LOW:
        cause = "low voltage"

    if recording_state == RecordingState.FILE_SIZE_LIMITED:
        cause = "file size limit"

    return f" Recording stopped due to {cause}."


def _get_battery_state_1_6_0(battery_state: ExtendedBatteryState) -> str:
    if battery_state == ExtendedBatteryState.AM_EXT_BAT_LOW:
        return "battery was less than 2.5V"

    if battery_state == ExtendedBatteryState.AM_EXT_BAT_FULL:
        return "battery was greater than 4.9V"

    voltage = battery_state.volts
    return f"battery was {voltage:01.01f}V"


def _get_frequency_filter_1_6_0(
    lower_filter_freq: int, higher_filter_freq: int
) -> str:
    """Get the frequency filter string.

    We assume that the filter frequencies are in units of Hz.
    """
    if lower_filter_freq == 0 and higher_filter_freq == 0:
        return ""

    low_freq = lower_filter_freq / 1000
    high_freq = higher_filter_freq / 1000

    if lower_filter_freq > 0 and higher_filter_freq > 0:
        return (
            " Band-pass filter with frequencies of "
            f"{low_freq:01.01f}kHz and {high_freq:01.01f}kHz applied."
        )

    if higher_filter_freq > 0:
        return (
            " Low-pass filter with frequency of "
            f"{high_freq:01.01f}kHz applied."
        )

    return (
        " High-pass filter with frequency of " f"{low_freq:01.01f}kHz applied."
    )


def generate_comment_v1_6_0(
    time: datetime.datetime,
    serial_number: int,
    extended_battery_state: ExtendedBatteryState,
    config: Config1_6_0,
    recording_state: RecordingState,
    temperature: float,
    deployment_id: Optional[int],
    external_microphone: bool,
):
    """Generate a comment in the format of the firmware version 1.6.0."""
    time_str = _get_datetime_1_0(time)
    timezone_str = _get_timezone_1_4_0(
        config.timezone_hours,
        config.timezone_minutes,
    )
    microphone_str = _get_microphone_1_5_0(external_microphone)
    artist_str = _get_artist_1_5_0(serial_number, deployment_id)
    gain_str = _get_gain_setting_1_6_0(config.gain)
    battery_str = _get_battery_state_1_6_0(extended_battery_state)
    temperature_str = _get_temperature_1_4_0(temperature)
    filter_str = _get_frequency_filter_1_6_0(
        config.lower_filter_freq,
        config.higher_filter_freq,
    )
    amplitude_threshold_str = _get_amplitude_threshold_1_6_0(
        config.amplitude_threshold,
        config.enable_amplitude_threshold_decibel_scale,
        config.enable_amplitude_threshold_percentage_scale,
        config.minimum_trigger_duration,
        config.amplitude_threshold_decibels,
        config.amplitude_threshold_percentage_mantissa,
        config.amplitude_threshold_percentage_exponent,
    )
    recording_state_str = _get_recording_state_1_6_0(recording_state)

    return (
        f"Recorded at {time_str} {timezone_str} {artist_str} {microphone_str}"
        f"at {gain_str} while {battery_str} "
        f"and {temperature_str}.{amplitude_threshold_str}"
        f"{filter_str}{recording_state_str}"
    )


def _get_gain_setting_1_7_0(gain: GainSetting) -> str:
    gain_str = ["low", "low-medium", "medium", "medium-high", "high"][
        gain.value
    ]
    return f"{gain_str} gain"


def _get_recording_state_1_7_0(recording_state: RecordingState) -> str:
    if recording_state == RecordingState.RECORDING_OKAY:
        return ""

    cause = "due to change of switch position"

    if recording_state == RecordingState.MICROPHONE_CHANGED:
        cause = "due to microphone change"

    if recording_state == RecordingState.MAGNETIC_SWITCH:
        cause = "by magnetic switch"

    if recording_state == RecordingState.SUPPLY_VOLTAGE_LOW:
        cause = "due to low voltage"

    if recording_state == RecordingState.FILE_SIZE_LIMITED:
        cause = "due to file size limit"

    return f" Recording stopped {cause}."


def generate_comment_v1_7_0(
    time: datetime.datetime,
    serial_number: int,
    extended_battery_state: ExtendedBatteryState,
    config: Config1_7_0,
    recording_state: RecordingState,
    temperature: float,
    deployment_id: Optional[int],
    external_microphone: bool,
):
    """Generate a comment in the format of the firmware version 1.7.0.

    Also valid for version 1.7.1
    """
    time_str = _get_datetime_1_0(time)
    timezone_str = _get_timezone_1_4_0(
        config.timezone_hours,
        config.timezone_minutes,
    )
    microphone_str = _get_microphone_1_5_0(external_microphone)
    artist_str = _get_artist_1_5_0(serial_number, deployment_id)
    gain_str = _get_gain_setting_1_7_0(config.gain)
    battery_str = _get_battery_state_1_4_0(extended_battery_state)
    temperature_str = _get_temperature_1_4_0(temperature)
    filter_str = _get_frequency_filter_1_6_0(
        config.lower_filter_freq,
        config.higher_filter_freq,
    )
    amplitude_threshold_str = _get_amplitude_threshold_1_6_0(
        config.amplitude_threshold,
        config.enable_amplitude_threshold_decibel_scale,
        config.enable_amplitude_threshold_percentage_scale,
        config.minimum_trigger_duration,
        config.amplitude_threshold_decibels,
        config.amplitude_threshold_percentage_mantissa,
        config.amplitude_threshold_percentage_exponent,
    )
    recording_state_str = _get_recording_state_1_7_0(recording_state)

    return (
        f"Recorded at {time_str} {timezone_str} {artist_str} {microphone_str}"
        f"at {gain_str} while {battery_str} "
        f"and {temperature_str}.{amplitude_threshold_str}"
        f"{filter_str}{recording_state_str}"
    )


def _get_frequency_trigger_1_8_0(
    enabled: bool,
    centre_frequency: int,
    window_length_shift: int,
    threshold_percentage_mantissa: int,
    threshold_percentage_exponent: int,
    minimum_trigger_duration: int,
) -> str:
    if not enabled:
        return ""

    threshold_str = _format_percentage(
        threshold_percentage_mantissa,
        threshold_percentage_exponent,
    )
    return (
        f" Frequency trigger ({centre_frequency / 10:.01f}kHz and window "
        f"length of {window_length_shift:d} samples) threshold was "
        f"{threshold_str} with {minimum_trigger_duration:d} minimum "
        "trigger duration."
    )


def generate_comment_v1_8_0(
    time: datetime.datetime,
    serial_number: int,
    extended_battery_state: ExtendedBatteryState,
    config: Config1_8_0,
    recording_state: RecordingState,
    temperature: float,
    deployment_id: Optional[int],
    external_microphone: bool,
):
    """Generate a comment in the format of the firmware version 1.8.0.

    Also valid for version 1.8.1
    """
    time_str = _get_datetime_1_0(time)
    timezone_str = _get_timezone_1_4_0(
        config.timezone_hours,
        config.timezone_minutes,
    )
    microphone_str = _get_microphone_1_5_0(external_microphone)
    artist_str = _get_artist_1_5_0(serial_number, deployment_id)
    gain_str = _get_gain_setting_1_7_0(config.gain)
    battery_str = _get_battery_state_1_4_0(extended_battery_state)
    temperature_str = _get_temperature_1_4_0(temperature)
    frequency_trigger_str = _get_frequency_trigger_1_8_0(
        config.enable_frequency_trigger,
        config.frequency_trigger_centre_frequency,
        config.frequency_trigger_window_length_shift,
        config.frequency_trigger_threshold_percentage_mantissa,
        config.frequency_trigger_threshold_percentage_exponent,
        config.minimum_trigger_duration,
    )
    filter_str = _get_frequency_filter_1_6_0(
        config.lower_filter_freq,
        config.higher_filter_freq,
    )
    amplitude_threshold_str = _get_amplitude_threshold_1_6_0(
        0 if config.enable_frequency_trigger else config.amplitude_threshold,
        config.enable_amplitude_threshold_decibel_scale,
        config.enable_amplitude_threshold_percentage_scale,
        config.minimum_trigger_duration,
        config.amplitude_threshold_decibels,
        config.amplitude_threshold_percentage_mantissa,
        config.amplitude_threshold_percentage_exponent,
    )
    recording_state_str = _get_recording_state_1_7_0(recording_state)

    return (
        f"Recorded at {time_str} {timezone_str} {artist_str} {microphone_str}"
        f"at {gain_str} while {battery_str} "
        f"and {temperature_str}.{frequency_trigger_str}"
        f"{amplitude_threshold_str}{filter_str}{recording_state_str}"
    )
