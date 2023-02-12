"""Test the parsing module."""
import datetime
from datetime import timedelta as td
from datetime import timezone as tz

from hypothesis import given
from hypothesis import strategies as st

from metamoth.config import Config1_0, Config1_2_0, Config1_2_1, Config1_2_2
from metamoth.enums import BatteryState, RecordingState
from metamoth.parsing import (
    parse_comment_version_1_0,
    parse_comment_version_1_0_1,
    parse_comment_version_1_2_0,
    parse_comment_version_1_2_1,
    parse_comment_version_1_2_2,
)

from .firmwares import (
    generate_comment_v1_0,
    generate_comment_v1_0_1,
    generate_comment_v1_2_0,
    generate_comment_v1_2_1,
    generate_comment_v1_2_2,
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
    config=st.builds(Config1_2_0, gain=st.integers(0, 4)),
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
    config=st.builds(Config1_2_1, gain=st.integers(0, 4)),
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
    assert parsed_comment.timezone == tz(td(0))
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
    config=st.builds(Config1_2_2, gain=st.integers(0, 4)),
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
    assert parsed_comment.timezone == tz(td(0))
    assert parsed_comment.audiomoth_id == f"{serial_number:016x}"
    assert parsed_comment.gain.value == config.gain
    assert parsed_comment.comment == comment
    assert parsed_comment.battery_state_v == battery_state.volts

    if battery_state == BatteryState.AM_BATTERY_LOW:
        assert parsed_comment.low_battery
    else:
        assert not parsed_comment.low_battery

    assert parsed_comment.recording_state == recording_state
