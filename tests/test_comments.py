"""Test comments module."""
import datetime
import os

from hypothesis import given
from hypothesis import strategies as st

from metamoth.chunks import parse_into_chunks
from metamoth.comments import (
    get_comments,
    parse_comment,
    parse_comment_version_1_0,
)
from metamoth.enums import BatteryState, GainSetting
from .firmwares import generate_comment_v1_0

PACKAGE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(PACKAGE_DIR, "data")
TEST_AUDIO = os.path.join(DATA_DIR, "test.wav")
TEST_COMMENT = (
    "Recorded at 19:17:30 06/04/2018 (UTC) by AudioMoth "
    "0FE081F80FE081F0 at gain setting 2 while battery "
    "state was 4.5V"
)


def test_parse_comment():
    """Test that comment can be parsed."""
    comment = parse_comment(TEST_COMMENT)

    assert comment.datetime == datetime.datetime(
        year=2018,
        month=4,
        day=6,
        hour=19,
        minute=17,
        second=30,
    )
    assert comment.timezone == "UTC"
    assert comment.audiomoth_id == "0FE081F80FE081F0"
    assert comment.gain == 2
    assert comment.battery_state == 4.5
    assert comment.comment == TEST_COMMENT


def test_get_comment_from_wav_file():
    """Test that comment can be parsed from WAV file."""
    with open(TEST_AUDIO, "rb") as wav:
        chunk = parse_into_chunks(wav)
        comment = get_comments(wav, chunk)

    assert comment.timezone == "UTC"
    assert comment.audiomoth_id == "0FE081F80FE081F0"
    assert comment.gain == 2
    assert comment.battery_state == 4.5
    assert comment.comment == TEST_COMMENT


@given(
    time=st.datetimes(),
    serial_number=st.integers(min_value=0, max_value=2**64 - 1),
    gain=st.sampled_from(GainSetting),
    battery_state=st.sampled_from(BatteryState),
)
def test_can_parse_comment_from_version_1_0(
    time: datetime.datetime,
    serial_number,
    gain,
    battery_state,
):
    """Test that comment can be parsed from firmware version 1.0."""
    time = time.replace(microsecond=0)

    comment = generate_comment_v1_0(
        time=time,
        serial_number=serial_number,
        gain=gain,
        battery_state=battery_state,
    )
    parsed_comment = parse_comment_version_1_0(comment)

    assert parsed_comment.datetime == time
    assert parsed_comment.timezone is None
    assert parsed_comment.audiomoth_id == f"{serial_number:016x}"
    assert parsed_comment.gain == gain.value
    assert parsed_comment.battery_state == battery_state.volts
    assert parsed_comment.comment == comment
