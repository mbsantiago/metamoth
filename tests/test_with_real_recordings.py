#!/usr/bin/env python

"""Tests for `metamoth` package."""

import os
from datetime import datetime as dt
from datetime import timezone as tz

from metamoth import parse_metadata
from metamoth.chunks import parse_into_chunks
from metamoth.comments import get_am_comment
from metamoth.enums import GainSetting, RecordingState
from metamoth.parsing import parse_comment_version_1_6_0

PACKAGE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(PACKAGE_DIR, "data")


def test_can_parse_1_6_0_comment():
    """Test that the AM comment from a v1_6_0 file can be parsed."""
    path = os.path.join(DATA_DIR, "20211112_193000.WAV")
    with open(path, "rb") as wav:
        chunks = parse_into_chunks(wav)
        comment = get_am_comment(wav, chunks)

    assert comment == (
        "Recorded at 19:30:00 12/11/2021 (UTC) by AudioMoth "
        "248D9B045EC9EE79 at medium gain while battery "
        "was 4.1V and temperature was 14.0C."
    )

    metadata = parse_comment_version_1_6_0(comment)

    assert metadata.timezone == tz.utc
    assert metadata.datetime == dt(2021, 11, 12, 19, 30)
    assert metadata.audiomoth_id == "248D9B045EC9EE79"
    assert metadata.gain == GainSetting.AM_GAIN_MEDIUM
    assert metadata.battery_state_v == 4.1
    assert metadata.comment == comment
    assert metadata.recording_state == RecordingState.RECORDING_OKAY


def test_can_parse_1_6_0_metadata():
    """Test that a v1_6_0 file can be parsed."""
    path = os.path.join(DATA_DIR, "20211112_193000.WAV")
    metadata = parse_metadata(path)

    assert metadata.timezone == tz.utc
    assert metadata.datetime == dt(2021, 11, 12, 19, 30)
    assert metadata.audiomoth_id == "248D9B045EC9EE79"
    assert metadata.gain == GainSetting.AM_GAIN_MEDIUM
    assert metadata.battery_state_v == 4.1
    assert metadata.comment == (
        "Recorded at 19:30:00 12/11/2021 (UTC) by AudioMoth "
        "248D9B045EC9EE79 at medium gain while battery "
        "was 4.1V and temperature was 14.0C."
    )
    assert metadata.recording_state == RecordingState.RECORDING_OKAY
