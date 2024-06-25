"""Test the parsing module."""

import datetime
import math
from datetime import timedelta as td
from datetime import timezone as tz
from typing import Optional

from hypothesis import given
from hypothesis import strategies as st
from metamoth.config import (
    Config1_0,
    Config1_2_0,
    Config1_2_1,
    Config1_2_2,
    Config1_4_0,
    Config1_6_0,
)
from metamoth.enums import (
    BatteryState,
    ExtendedBatteryState,
    FilterType,
    RecordingState,
)
from metamoth.parsing import (
    db_to_amplitude,
    parse_comment_version_1_0,
    parse_comment_version_1_0_1,
    parse_comment_version_1_2_0,
    parse_comment_version_1_2_1,
    parse_comment_version_1_2_2,
    parse_comment_version_1_4_0,
    parse_comment_version_1_4_2,
    parse_comment_version_1_6_0,
    percentage_to_amplitude,
)

from .firmwares import (
    generate_comment_v1_0,
    generate_comment_v1_0_1,
    generate_comment_v1_2_0,
    generate_comment_v1_2_1,
    generate_comment_v1_2_2,
    generate_comment_v1_4_0,
    generate_comment_v1_4_2,
    generate_comment_v1_6_0,
)


@given(
    time=st.datetimes(),
    serial_number=st.integers(min_value=0, max_value=2**64 - 1),
    battery_state=st.sampled_from(BatteryState),
    config=st.builds(Config1_0, gain=st.integers(0, 4)),
)
def test_can_parse_comment_from_version_1_0(
    time: datetime.datetime,
    serial_number,
    battery_state,
    config,
):
    """Test that comment can be parsed from firmware version 1.0."""
    time = time.replace(microsecond=0)

    comment = generate_comment_v1_0(
        time=time,
        serial_number=serial_number,
        battery_state=battery_state,
        config=config,
    )
    parsed_comment = parse_comment_version_1_0(comment)

    assert parsed_comment.datetime == time
    assert parsed_comment.timezone == tz(td(0))
    assert parsed_comment.audiomoth_id == f"{serial_number:016x}"
    assert parsed_comment.gain.value == config.gain
    assert parsed_comment.comment == comment
    assert parsed_comment.battery_state_v == battery_state.volts

    if battery_state == BatteryState.AM_BATTERY_LOW:
        assert parsed_comment.low_battery
    else:
        assert not parsed_comment.low_battery


@given(
    time=st.datetimes(),
    serial_number=st.integers(min_value=0, max_value=2**64 - 1),
    battery_state=st.sampled_from(BatteryState),
    config=st.builds(Config1_0, gain=st.integers(0, 4)),
)
def test_can_parse_comment_from_version_1_0_1(
    time: datetime.datetime,
    serial_number,
    battery_state,
    config,
):
    """Test that comment can be parsed from firmware version 1.0.1.

    Also valid for version 1.1.0.
    """
    time = time.replace(microsecond=0)

    comment = generate_comment_v1_0_1(
        time=time,
        serial_number=serial_number,
        battery_state=battery_state,
        config=config,
    )
    parsed_comment = parse_comment_version_1_0_1(comment)

    assert parsed_comment.datetime == time
    assert parsed_comment.timezone == tz(td(0))
    assert parsed_comment.audiomoth_id == f"{serial_number:016x}"
    assert parsed_comment.gain.value == config.gain
    assert parsed_comment.comment == comment
    assert parsed_comment.battery_state_v == battery_state.volts

    if battery_state == BatteryState.AM_BATTERY_LOW:
        assert parsed_comment.low_battery
    else:
        assert not parsed_comment.low_battery


@given(
    time=st.datetimes(),
    serial_number=st.integers(min_value=0, max_value=2**64 - 1),
    battery_state=st.sampled_from(BatteryState),
    config=st.builds(
        Config1_2_0,
        gain=st.integers(0, 4),
        timezone=st.integers(-12, 12),
    ),
)
def test_can_parse_comment_from_version_1_2_0(
    time: datetime.datetime,
    serial_number: int,
    battery_state: BatteryState,
    config: Config1_2_0,
):
    """Test that comment can be parsed from firmware version 1.2.0."""
    time = time.replace(microsecond=0)

    comment = generate_comment_v1_2_0(
        time=time,
        serial_number=serial_number,
        battery_state=battery_state,
        config=config,
    )
    parsed_comment = parse_comment_version_1_2_0(comment)

    assert parsed_comment.datetime == time
    assert parsed_comment.timezone == tz(td(hours=config.timezone))
    assert parsed_comment.audiomoth_id == f"{serial_number:016x}"
    assert parsed_comment.gain.value == config.gain
    assert parsed_comment.comment == comment
    assert parsed_comment.battery_state_v == battery_state.volts

    if battery_state == BatteryState.AM_BATTERY_LOW:
        assert parsed_comment.low_battery
    else:
        assert not parsed_comment.low_battery


@given(
    time=st.datetimes(),
    serial_number=st.integers(min_value=0, max_value=2**64 - 1),
    battery_state=st.sampled_from(BatteryState),
    config=st.builds(
        Config1_2_1,
        gain=st.integers(0, 4),
        timezone=st.integers(-12, 12),
    ),
    recording_state=st.sampled_from(
        [
            RecordingState.RECORDING_OKAY,
            RecordingState.SWITCH_CHANGED,
            RecordingState.SUPPLY_VOLTAGE_LOW,
        ]
    ),
)
def test_can_parse_comment_from_version_1_2_1(
    time: datetime.datetime,
    serial_number: int,
    battery_state: BatteryState,
    config: Config1_2_1,
    recording_state: RecordingState,
):
    """Test that comment can be parsed from firmware version 1.2.1."""
    time = time.replace(microsecond=0)

    comment = generate_comment_v1_2_1(
        time=time,
        serial_number=serial_number,
        battery_state=battery_state,
        config=config,
        recording_state=recording_state,
    )
    parsed_comment = parse_comment_version_1_2_1(comment)

    assert parsed_comment.datetime == time
    assert parsed_comment.timezone == tz(td(hours=config.timezone))
    assert parsed_comment.audiomoth_id == f"{serial_number:016x}"
    assert parsed_comment.gain.value == config.gain
    assert parsed_comment.comment == comment
    assert parsed_comment.battery_state_v == battery_state.volts

    if battery_state == BatteryState.AM_BATTERY_LOW:
        assert parsed_comment.low_battery
    else:
        assert not parsed_comment.low_battery

    assert parsed_comment.recording_state == recording_state


@given(
    time=st.datetimes(),
    serial_number=st.integers(min_value=0, max_value=2**64 - 1),
    battery_state=st.sampled_from(BatteryState),
    config=st.builds(
        Config1_2_2,
        gain=st.integers(0, 4),
        timezone_hours=st.integers(-12, 12),
        timezone_minutes=st.integers(0, 59),
    ),
    recording_state=st.sampled_from(
        [
            RecordingState.RECORDING_OKAY,
            RecordingState.SWITCH_CHANGED,
            RecordingState.SUPPLY_VOLTAGE_LOW,
        ]
    ),
)
def test_can_parse_comment_from_version_1_2_2(
    time: datetime.datetime,
    serial_number: int,
    battery_state: BatteryState,
    config: Config1_2_2,
    recording_state: RecordingState,
):
    """Test that comment can be parsed from firmware version 1.2.2.

    Also applies to version 1.3.0.
    """
    time = time.replace(microsecond=0)

    comment = generate_comment_v1_2_2(
        time=time,
        serial_number=serial_number,
        battery_state=battery_state,
        config=config,
        recording_state=recording_state,
    )
    parsed_comment = parse_comment_version_1_2_2(comment)

    assert parsed_comment.datetime == time
    assert parsed_comment.timezone == tz(
        td(hours=config.timezone_hours, minutes=config.timezone_minutes)
    )
    assert parsed_comment.audiomoth_id == f"{serial_number:016x}"
    assert parsed_comment.gain.value == config.gain
    assert parsed_comment.comment == comment
    assert parsed_comment.battery_state_v == battery_state.volts

    if battery_state == BatteryState.AM_BATTERY_LOW:
        assert parsed_comment.low_battery
    else:
        assert not parsed_comment.low_battery

    assert parsed_comment.recording_state == recording_state


@given(
    time=st.datetimes(),
    serial_number=st.integers(min_value=0, max_value=2**64 - 1),
    battery_state=st.sampled_from(ExtendedBatteryState),
    config=st.builds(
        Config1_4_0,
        gain=st.integers(0, 4),
        timezone_hours=st.integers(-12, 12),
        timezone_minutes=st.integers(0, 59),
        amplitude_threshold=st.integers(0, 100),
        higher_filter_freq=st.integers(0, 20000),
        lower_filter_freq=st.integers(0, 20000),
    ),
    recording_state=st.sampled_from(
        [
            RecordingState.RECORDING_OKAY,
            RecordingState.SWITCH_CHANGED,
            RecordingState.SUPPLY_VOLTAGE_LOW,
        ]
    ),
    temperature=st.integers(min_value=-10, max_value=50),
)
def test_can_parse_comment_from_version_1_4_0(
    time: datetime.datetime,
    serial_number: int,
    battery_state: ExtendedBatteryState,
    config: Config1_4_0,
    recording_state: RecordingState,
    temperature: int,
):
    """Test that comment can be parsed from firmware version 1.4.0.

    Also applies to version 1.4.1.
    """
    time = time.replace(microsecond=0)

    comment = generate_comment_v1_4_0(
        time=time,
        serial_number=serial_number,
        extended_battery_state=battery_state,
        config=config,
        recording_state=recording_state,
        temperature=temperature,
    )
    parsed_comment = parse_comment_version_1_4_0(comment)

    assert parsed_comment.datetime == time
    assert parsed_comment.timezone == tz(
        td(hours=config.timezone_hours, minutes=config.timezone_minutes)
    )
    assert parsed_comment.audiomoth_id == f"{serial_number:016x}"
    assert parsed_comment.gain.value == config.gain
    assert parsed_comment.comment == comment
    assert parsed_comment.battery_state_v == battery_state.volts

    if battery_state == ExtendedBatteryState.AM_EXT_BAT_LOW:
        assert parsed_comment.low_battery
    else:
        assert not parsed_comment.low_battery

    assert parsed_comment.temperature_c == temperature
    assert parsed_comment.amplitude_threshold.enabled == (
        config.amplitude_threshold > 0
    )

    filter_type = FilterType.NO_FILTER
    if config.higher_filter_freq > 0 and config.lower_filter_freq > 0:
        filter_type = FilterType.BAND_PASS
    elif config.higher_filter_freq > 0:
        filter_type = FilterType.LOW_PASS
    elif config.lower_filter_freq > 0:
        filter_type = FilterType.HIGH_PASS

    assert parsed_comment.frequency_filter.type == filter_type

    if filter_type in [FilterType.BAND_PASS, FilterType.LOW_PASS]:
        assert parsed_comment.frequency_filter.higher_frequency_hz == int(
            1000 * float(f"{config.higher_filter_freq / 1000:.1f}")
        )
    else:
        assert parsed_comment.frequency_filter.higher_frequency_hz is None

    if filter_type in [FilterType.BAND_PASS, FilterType.HIGH_PASS]:
        assert parsed_comment.frequency_filter.lower_frequency_hz == int(
            1000 * float(f"{config.lower_filter_freq / 1000:.1f}")
        )
    else:
        assert parsed_comment.frequency_filter.lower_frequency_hz is None


@given(
    time=st.datetimes(),
    serial_number=st.integers(min_value=0, max_value=2**64 - 1),
    battery_state=st.sampled_from(ExtendedBatteryState),
    config=st.builds(
        Config1_4_0,
        gain=st.integers(0, 4),
        timezone_hours=st.integers(-12, 12),
        timezone_minutes=st.integers(0, 59),
        amplitude_threshold=st.integers(0, 100),
        higher_filter_freq=st.integers(0, 20000),
        lower_filter_freq=st.integers(0, 20000),
    ),
    recording_state=st.sampled_from(
        [
            RecordingState.RECORDING_OKAY,
            RecordingState.SWITCH_CHANGED,
            RecordingState.SUPPLY_VOLTAGE_LOW,
            RecordingState.FILE_SIZE_LIMITED,
        ]
    ),
    temperature=st.integers(min_value=-10, max_value=50),
)
def test_can_parse_comment_from_version_1_4_2(
    time: datetime.datetime,
    serial_number: int,
    battery_state: ExtendedBatteryState,
    config: Config1_4_0,
    recording_state: RecordingState,
    temperature: int,
):
    """Test that comment can be parsed from firmware version 1.4.2.

    Also applies to version 1.4.3.
    """
    time = time.replace(microsecond=0)

    comment = generate_comment_v1_4_2(
        time=time,
        serial_number=serial_number,
        extended_battery_state=battery_state,
        config=config,
        recording_state=recording_state,
        temperature=temperature,
    )
    parsed_comment = parse_comment_version_1_4_2(comment)

    assert parsed_comment.datetime == time

    assert parsed_comment.timezone == tz(
        td(hours=config.timezone_hours, minutes=config.timezone_minutes)
    )
    assert parsed_comment.audiomoth_id == f"{serial_number:016x}"
    assert parsed_comment.gain.value == config.gain
    assert parsed_comment.comment == comment
    assert parsed_comment.battery_state_v == battery_state.volts

    if battery_state == ExtendedBatteryState.AM_EXT_BAT_LOW:
        assert parsed_comment.low_battery
    else:
        assert not parsed_comment.low_battery

    assert parsed_comment.recording_state == recording_state
    assert parsed_comment.temperature_c == temperature
    assert parsed_comment.amplitude_threshold.enabled == (
        config.amplitude_threshold > 0
    )

    filter_type = FilterType.NO_FILTER
    if config.higher_filter_freq > 0 and config.lower_filter_freq > 0:
        filter_type = FilterType.BAND_PASS
    elif config.higher_filter_freq > 0:
        filter_type = FilterType.LOW_PASS
    elif config.lower_filter_freq > 0:
        filter_type = FilterType.HIGH_PASS

    assert parsed_comment.frequency_filter.type == filter_type

    if filter_type in [FilterType.BAND_PASS, FilterType.LOW_PASS]:
        assert parsed_comment.frequency_filter.higher_frequency_hz == int(
            1000 * float(f"{config.higher_filter_freq / 1000:.1f}")
        )
    else:
        assert parsed_comment.frequency_filter.higher_frequency_hz is None

    if filter_type in [FilterType.BAND_PASS, FilterType.HIGH_PASS]:
        assert parsed_comment.frequency_filter.lower_frequency_hz == int(
            1000 * float(f"{config.lower_filter_freq / 1000:.1f}")
        )
    else:
        assert parsed_comment.frequency_filter.lower_frequency_hz is None


@given(
    time=st.datetimes(),
    serial_number=st.integers(min_value=0, max_value=2**64 - 1),
    battery_state=st.sampled_from(ExtendedBatteryState),
    config=st.builds(
        Config1_6_0,
        gain=st.integers(0, 4),
        timezone_hours=st.integers(-12, 12),
        timezone_minutes=st.integers(0, 59),
        amplitude_threshold=st.integers(0, 100),
        higher_filter_freq=st.integers(0, 20000),
        lower_filter_freq=st.integers(0, 20000),
        minimum_trigger_duration=st.integers(0, 100),
        enable_amplitude_threshold_decibel_scale=st.booleans(),
        amplitude_threshold_decibels=st.integers(0, 100),
        enable_amplitude_threshold_percentage_scale=st.booleans(),
        amplitude_threshold_percentage_mantissa=st.integers(0, 100),
        amplitude_threshold_percentage_exponent=st.integers(-2, 4),
    ),
    recording_state=st.sampled_from(
        [
            RecordingState.RECORDING_OKAY,
            RecordingState.SWITCH_CHANGED,
            RecordingState.SUPPLY_VOLTAGE_LOW,
            RecordingState.FILE_SIZE_LIMITED,
        ]
    ),
    temperature=st.integers(min_value=-10, max_value=50),
    deployment_id=st.integers(min_value=0, max_value=2**32 - 1) | st.none(),
    external_microphone=st.booleans(),
)
def test_can_parse_comment_from_version_1_6_0(
    time: datetime.datetime,
    serial_number: int,
    battery_state: ExtendedBatteryState,
    config: Config1_6_0,
    recording_state: RecordingState,
    temperature: int,
    deployment_id: Optional[int],
    external_microphone: bool,
):
    """Test that comment can be parsed from firmware version 1.6.0."""
    time = time.replace(microsecond=0)

    comment = generate_comment_v1_6_0(
        time=time,
        serial_number=serial_number,
        extended_battery_state=battery_state,
        config=config,
        recording_state=recording_state,
        temperature=temperature,
        deployment_id=deployment_id,
        external_microphone=external_microphone,
    )
    parsed_comment = parse_comment_version_1_6_0(comment)

    assert parsed_comment.datetime == time

    assert parsed_comment.timezone == tz(
        td(hours=config.timezone_hours, minutes=config.timezone_minutes)
    )
    assert parsed_comment.audiomoth_id == (
        f"{deployment_id:016x}"
        if deployment_id is not None
        else f"{serial_number:016x}"
    )
    assert parsed_comment.deployment_id == (
        f"{deployment_id:016x}" if deployment_id is not None else None
    )
    assert parsed_comment.gain.value == config.gain
    assert parsed_comment.comment == comment
    assert parsed_comment.battery_state_v == battery_state.volts

    if battery_state == ExtendedBatteryState.AM_EXT_BAT_LOW:
        assert parsed_comment.low_battery
    else:
        assert not parsed_comment.low_battery

    assert parsed_comment.recording_state == recording_state
    assert parsed_comment.temperature_c == temperature

    threshold_enabled = (
        config.amplitude_threshold > 0
        or config.enable_amplitude_threshold_decibel_scale
        or config.enable_amplitude_threshold_percentage_scale
    )

    assert parsed_comment.amplitude_threshold.enabled == threshold_enabled

    if threshold_enabled:
        assert (
            parsed_comment.minimum_trigger_duration_s
            == config.minimum_trigger_duration
        )

    filter_type = FilterType.NO_FILTER
    if config.higher_filter_freq > 0 and config.lower_filter_freq > 0:
        filter_type = FilterType.BAND_PASS
    elif config.higher_filter_freq > 0:
        filter_type = FilterType.LOW_PASS
    elif config.lower_filter_freq > 0:
        filter_type = FilterType.HIGH_PASS

    assert parsed_comment.frequency_filter.type == filter_type

    if filter_type in [FilterType.BAND_PASS, FilterType.LOW_PASS]:
        assert parsed_comment.frequency_filter.higher_frequency_hz == int(
            1000 * float(f"{config.higher_filter_freq / 1000:.1f}")
        )
    else:
        assert parsed_comment.frequency_filter.higher_frequency_hz is None

    if filter_type in [FilterType.BAND_PASS, FilterType.HIGH_PASS]:
        assert parsed_comment.frequency_filter.lower_frequency_hz == int(
            1000 * float(f"{config.lower_filter_freq / 1000:.1f}")
        )
    else:
        assert parsed_comment.frequency_filter.lower_frequency_hz is None


def format_percentage(mantissa: int, exponent: int) -> float:
    response = ""

    if exponent < 0:
        response += "0.0000"[: 1 - exponent]

    response += str(mantissa)

    for _ in range(exponent):
        response += "0"

    return float(response)


@given(
    slider=st.floats(min_value=0, max_value=1),
)
def test_convert_amplitude_functions(slider: float):
    """Test that amplitude conversion functions work as expected.

    The following code is taken from the AudioMoth Configuration App.
    In the app UI you can adjust the amplitude threshold using a slider.
    The slider value is converted to equivalent decibels, percentage and
    amplitude values.

    Here we use the same code to test that the conversion functions work
    as expected.
    """
    raw_log = 100 * slider - 100
    exponent = 2 + math.floor(raw_log / 20)
    mantissa = round(10 ** ((raw_log / 20) - exponent + 2))

    if mantissa == 0:
        mantissa = 1
        exponent += 1

    decibel = raw_log
    percentage = format_percentage(mantissa, exponent)
    amplitude = round(32768 * 10 ** (raw_log / 20))

    recovered_amplitude = db_to_amplitude(decibel)
    recovered_percentage = percentage_to_amplitude(percentage)

    if amplitude == 0:
        assert recovered_amplitude == 0
        assert recovered_percentage < 2

    else:
        assert abs(amplitude - recovered_amplitude) < 2 * 10 ** (4 - exponent)
        assert abs(amplitude - recovered_percentage) < 2 * 10 ** (4 - exponent)
