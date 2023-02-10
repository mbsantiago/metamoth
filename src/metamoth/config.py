"""Module with AudioMoth configuration classes for different versions."""
# pylint: disable=too-many-instance-attributes,invalid-name

from dataclasses import dataclass, field
from typing import List

from metamoth.enums import BatteryLevelDisplayType, GainSetting

__all__ = [
    "Config1_0",
    "Config1_1_0",
    "Config1_2_0",
    "Config1_2_1",
    "Config1_2_2",
    "Config1_4_0",
    "Config1_5_0",
    "Config1_6_0",
    "Config1_7_0",
    "Config1_8_0",
]


@dataclass
class StartStopPeriod:
    """Start/stop period for a recording."""

    start_minutes: int
    stop_minutes: int


@dataclass
class Config1_0:
    """AudioMoth configuration for version 1.0.

    Also valid for version 1.0.1
    """

    time: int = 0
    gain: int = 2
    clock_band: int = 4
    clock_divider: int = 2
    acquisition_cycles: int = 2
    oversample_rate: int = 16
    sample_rate: int = 48000
    sleep_duration: int = 0
    record_duration: int = 60
    enable_led: bool = True
    active_start_stop_periods: bool = False
    start_stop_period: List[StartStopPeriod] = field(
        default_factory=lambda: [
            StartStopPeriod(start_minutes=60, stop_minutes=120),
            StartStopPeriod(start_minutes=300, stop_minutes=420),
            StartStopPeriod(start_minutes=540, stop_minutes=600),
            StartStopPeriod(start_minutes=720, stop_minutes=780),
            StartStopPeriod(start_minutes=900, stop_minutes=960),
        ]
    )


@dataclass
class Config1_1_0:
    """AudioMoth configuration for version 1.1.0."""

    time: int = 0
    gain: int = 2
    clock_divider: int = 4
    acquisition_cycles: int = 16
    oversample_rate: int = 1
    sample_rate: int = 384000
    sample_rate_divider: int = 8
    sleep_duration: int = 0
    record_duration: int = 60
    enable_led: bool = True
    active_start_stop_periods: bool = False
    start_stop_period: List[StartStopPeriod] = field(
        default_factory=lambda: [
            StartStopPeriod(start_minutes=60, stop_minutes=120),
            StartStopPeriod(start_minutes=300, stop_minutes=420),
            StartStopPeriod(start_minutes=540, stop_minutes=600),
            StartStopPeriod(start_minutes=720, stop_minutes=780),
            StartStopPeriod(start_minutes=900, stop_minutes=960),
        ]
    )


@dataclass
class Config1_2_0:
    """AudioMoth configuration for version 1.2.0."""

    time: int = 0
    gain: int = 2
    clock_divider: int = 4
    acquisition_cycles: int = 16
    oversample_rate: int = 1
    sample_rate: int = 384000
    sleep_duration: int = 0
    record_duration: int = 60
    enable_led: bool = True
    active_start_stop_periods: bool = False
    start_stop_period: List[StartStopPeriod] = field(
        default_factory=lambda: [
            StartStopPeriod(start_minutes=60, stop_minutes=120),
            StartStopPeriod(start_minutes=300, stop_minutes=420),
            StartStopPeriod(start_minutes=540, stop_minutes=600),
            StartStopPeriod(start_minutes=720, stop_minutes=780),
            StartStopPeriod(start_minutes=900, stop_minutes=960),
        ]
    )
    timezone: int = 0


@dataclass
class Config1_2_1:
    """AudioMoth configuration for version 1.2.1."""

    time: int = 0
    gain: int = 2
    clock_divider: int = 4
    acquisition_cycles: int = 16
    oversample_rate: int = 1
    sample_rate: int = 384000
    sleep_duration: int = 0
    record_duration: int = 60
    enable_led: bool = True
    active_start_stop_periods: bool = False
    start_stop_period: List[StartStopPeriod] = field(
        default_factory=lambda: [
            StartStopPeriod(start_minutes=60, stop_minutes=120),
            StartStopPeriod(start_minutes=300, stop_minutes=420),
            StartStopPeriod(start_minutes=540, stop_minutes=600),
            StartStopPeriod(start_minutes=720, stop_minutes=780),
            StartStopPeriod(start_minutes=900, stop_minutes=960),
        ]
    )
    timezone: int = 0
    enable_battery_check: bool = False
    disable_battery_level_display: bool = False


@dataclass
class Config1_2_2:
    """AudioMoth configuration for version 1.2.2.

    Also valid for version 1.3.0.
    """

    time: int = 0
    gain: int = 2
    clock_divider: int = 4
    acquisition_cycles: int = 16
    oversample_rate: int = 1
    sample_rate: int = 384000
    sample_rate_divider: int = 8
    sleep_duration: int = 0
    record_duration: int = 60
    enable_led: bool = True
    active_start_stop_periods: bool = False
    start_stop_period: List[StartStopPeriod] = field(
        default_factory=lambda: [
            StartStopPeriod(start_minutes=60, stop_minutes=120),
            StartStopPeriod(start_minutes=300, stop_minutes=420),
            StartStopPeriod(start_minutes=540, stop_minutes=600),
            StartStopPeriod(start_minutes=720, stop_minutes=780),
            StartStopPeriod(start_minutes=900, stop_minutes=960),
        ]
    )
    timezone_hours: int = 0
    enable_battery_check: bool = False
    disable_battery_level_display: bool = False
    timezone_minutes: int = 0


@dataclass
class Config1_4_0:
    """AudioMoth configuration for version 1.4.0.

    Also valid for version 1.4.1, 1.4.2, 1.4.3, 1.4.4,
    """

    time: int = 0
    gain: int = 2
    clock_divider: int = 4
    acquisition_cycles: int = 16
    oversample_rate: int = 1
    sample_rate: int = 384000
    sample_rate_divider: int = 8
    sleep_duration: int = 5
    record_duration: int = 55
    enable_led: bool = True
    active_start_stop_periods: bool = False
    start_stop_period: List[StartStopPeriod] = field(
        default_factory=lambda: [
            StartStopPeriod(start_minutes=0, stop_minutes=60),
            StartStopPeriod(start_minutes=120, stop_minutes=180),
            StartStopPeriod(start_minutes=240, stop_minutes=300),
            StartStopPeriod(start_minutes=360, stop_minutes=420),
            StartStopPeriod(start_minutes=480, stop_minutes=540),
        ]
    )
    timezone_hours: int = 0
    enable_low_voltage_cutoff: bool = False
    disable_battery_level_display: bool = False
    timezone_minutes: int = 0
    disable_sleep_record_cycle: bool = False
    earliest_recording_time: int = 0
    latest_recording_time: int = 0
    lower_filter_freq: int = 0
    higher_filter_freq: int = 0
    amplitude_threshold: int = 0


@dataclass
class Config1_5_0:
    """AudioMoth configuration for version 1.5.0."""

    time: int = 0
    gain: int = 2
    clock_divider: int = 4
    acquisition_cycles: int = 16
    oversample_rate: int = 1
    sample_rate: int = 384000
    sample_rate_divider: int = 8
    sleep_duration: int = 5
    record_duration: int = 55
    enable_led: bool = True
    active_start_stop_periods: bool = False
    start_stop_period: List[StartStopPeriod] = field(
        default_factory=lambda: [
            StartStopPeriod(start_minutes=0, stop_minutes=60),
            StartStopPeriod(start_minutes=120, stop_minutes=180),
            StartStopPeriod(start_minutes=240, stop_minutes=300),
            StartStopPeriod(start_minutes=360, stop_minutes=420),
            StartStopPeriod(start_minutes=480, stop_minutes=540),
        ]
    )
    timezone_hours: int = 0
    enable_low_voltage_cutoff: bool = False
    disable_battery_level_display: bool = False
    timezone_minutes: int = 0
    disable_sleep_record_cycle: bool = False
    earliest_recording_time: int = 0
    latest_recording_time: int = 0
    lower_filter_freq: int = 0
    higher_filter_freq: int = 0
    amplitude_threshold: int = 0
    require_acoustic_configuration: bool = False
    battery_level_display_type: BatteryLevelDisplayType = (
        BatteryLevelDisplayType.BATTERY_LEVEL
    )
    minimum_amplitude_threshold_duration: int = 0


@dataclass
class Config1_6_0:
    """AudioMoth configuration for version 1.6.0."""

    time: int = 0
    gain: int = 2
    clock_divider: int = 4
    acquisition_cycles: int = 16
    oversample_rate: int = 1
    sample_rate: int = 384000
    sample_rate_divider: int = 8
    sleep_duration: int = 5
    record_duration: int = 55
    enable_led: bool = True
    active_start_stop_periods: bool = True
    start_stop_period: List[StartStopPeriod] = field(
        default_factory=lambda: [
            StartStopPeriod(start_minutes=0, stop_minutes=1440),
            StartStopPeriod(start_minutes=0, stop_minutes=1440),
            StartStopPeriod(start_minutes=0, stop_minutes=1440),
            StartStopPeriod(start_minutes=0, stop_minutes=1440),
            StartStopPeriod(start_minutes=0, stop_minutes=1440),
        ]
    )
    timezone_hours: int = 0
    enable_low_voltage_cutoff: bool = True
    disable_battery_level_display: bool = False
    timezone_minutes: int = 0
    disable_sleep_record_cycle: bool = False
    earliest_recording_time: int = 0
    latest_recording_time: int = 0
    lower_filter_freq: int = 0
    higher_filter_freq: int = 0
    amplitude_threshold: int = 0
    require_acoustic_configuration: bool = False
    battery_level_display_type: BatteryLevelDisplayType = (
        BatteryLevelDisplayType.BATTERY_LEVEL
    )
    minimum_trigger_duration: int = 0
    enable_amplitude_threshold_decibel_scale: bool = False
    amplitude_threshold_decibels: int = 0
    enable_amplitude_threshold_percentage_scale: bool = False
    amplitude_threshold_percentage_mantissa: int = 0
    amplitude_threshold_percentage_exponent: int = 0
    enable_energy_saver_mode: bool = False
    disable_48_hz_dc_blocking_filter: bool = False


@dataclass
class Config1_7_0:
    """AudioMoth configuration for version 1.7.0.

    Also valid for version 1.7.1.
    """

    time: int = 0
    gain: GainSetting = GainSetting.AM_GAIN_MEDIUM
    clock_divider: int = 4
    acquisition_cycles: int = 16
    oversample_rate: int = 1
    sample_rate: int = 384000
    sample_rate_divider: int = 8
    sleep_duration: int = 5
    record_duration: int = 55
    enable_led: bool = True
    active_start_stop_periods: bool = True
    start_stop_period: List[StartStopPeriod] = field(
        default_factory=lambda: [
            StartStopPeriod(start_minutes=0, stop_minutes=1440),
            StartStopPeriod(start_minutes=0, stop_minutes=1440),
            StartStopPeriod(start_minutes=0, stop_minutes=1440),
            StartStopPeriod(start_minutes=0, stop_minutes=1440),
            StartStopPeriod(start_minutes=0, stop_minutes=1440),
        ]
    )
    timezone_hours: int = 0
    enable_low_voltage_cutoff: bool = True
    disable_battery_level_display: bool = False
    timezone_minutes: int = 0
    disable_sleep_record_cycle: bool = False
    earliest_recording_time: int = 0
    latest_recording_time: int = 0
    lower_filter_freq: int = 0
    higher_filter_freq: int = 0
    amplitude_threshold: int = 0
    require_acoustic_configuration: bool = False
    battery_level_display_type: BatteryLevelDisplayType = (
        BatteryLevelDisplayType.BATTERY_LEVEL
    )
    minimum_trigger_duration: int = 0
    enable_amplitude_threshold_decibel_scale: bool = False
    amplitude_threshold_decibels: int = 0
    enable_amplitude_threshold_percentage_scale: bool = False
    amplitude_threshold_percentage_mantissa: int = 0
    amplitude_threshold_percentage_exponent: int = 0
    enable_energy_saver_mode: bool = False
    disable_48_hz_dc_blocking_filter: bool = False
    enable_time_settings_from_gps: bool = False
    enable_magnetic_switch: bool = False
    enable_low_gain_range: bool = False


@dataclass
class Config1_8_0:
    """AudioMoth configuration for version 1.8.0.

    Also valid for version 1.8.1.
    """

    time: int = 0
    gain: GainSetting = GainSetting.AM_GAIN_MEDIUM
    clock_divider: int = 4
    acquisition_cycles: int = 16
    oversample_rate: int = 1
    sample_rate: int = 384000
    sample_rate_divider: int = 8
    sleep_duration: int = 5
    record_duration: int = 55
    enable_led: bool = True
    active_start_stop_periods: bool = True
    start_stop_period: List[StartStopPeriod] = field(
        default_factory=lambda: [
            StartStopPeriod(start_minutes=0, stop_minutes=1440),
            StartStopPeriod(start_minutes=0, stop_minutes=1440),
            StartStopPeriod(start_minutes=0, stop_minutes=1440),
            StartStopPeriod(start_minutes=0, stop_minutes=1440),
            StartStopPeriod(start_minutes=0, stop_minutes=1440),
        ]
    )
    timezone_hours: int = 0
    enable_low_voltage_cutoff: bool = True
    disable_battery_level_display: bool = False
    timezone_minutes: int = 0
    disable_sleep_record_cycle: bool = False
    earliest_recording_time: int = 0
    latest_recording_time: int = 0
    lower_filter_freq: int = 0
    higher_filter_freq: int = 0
    amplitude_threshold: int = 0
    frequency_trigger_centre_frequency: int = 0
    require_acoustic_configuration: bool = False
    battery_level_display_type: BatteryLevelDisplayType = (
        BatteryLevelDisplayType.BATTERY_LEVEL
    )
    minimum_trigger_duration: int = 0
    frequency_trigger_window_length_shift: int = 0
    frequency_trigger_threshold_percentage_mantissa: int = 0
    frequency_trigger_threshold_percentage_exponent: int = 0
    enable_amplitude_threshold_decibel_scale: bool = False
    amplitude_threshold_decibels: int = 0
    enable_amplitude_threshold_percentage_scale: bool = False
    amplitude_threshold_percentage_mantissa: int = 0
    amplitude_threshold_percentage_exponent: int = 0
    enable_energy_saver_mode: bool = False
    disable_48_hz_dc_blocking_filter: bool = False
    enable_time_settings_from_gps: bool = False
    enable_magnetic_switch: bool = False
    enable_low_gain_range: bool = False
    enable_frequency_trigger: bool = False
    enable_daily_folders: bool = False
