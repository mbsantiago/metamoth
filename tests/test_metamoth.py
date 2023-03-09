#!/usr/bin/env python

"""Tests for `metamoth` package."""

import os
from datetime import datetime as dt
from datetime import timezone as tz

from metamoth import parse_metadata
from metamoth.enums import GainSetting, RecordingState

PACKAGE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(PACKAGE_DIR, "data")
TEST_AUDIO = os.path.join(DATA_DIR, "test.wav")


def test_parse_metadata():
    """Test that metadata can be parsed from WAV file."""
    metadata = parse_metadata(TEST_AUDIO)

    assert metadata.path == str(TEST_AUDIO)
    assert metadata.timezone == tz.utc
    assert metadata.datetime == dt(2018, 4, 6, 19, 17, 30)
    assert metadata.audiomoth_id == "0FE081F80FE081F0"
    assert metadata.gain == GainSetting.AM_GAIN_MEDIUM
    assert metadata.battery_state_v == 4.5
    assert metadata.comment == (
        "Recorded at 19:17:30 06/04/2018 (UTC) by AudioMoth "
        "0FE081F80FE081F0 at gain setting 2 while battery "
        "state was 4.5V"
    )
    assert metadata.samplerate_hz == 192000
    assert metadata.channels == 1
    assert metadata.samples == 3840000
    assert metadata.duration_s == 20.0
    assert metadata.recording_state == RecordingState.RECORDING_OKAY
