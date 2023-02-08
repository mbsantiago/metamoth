#!/usr/bin/env python

"""Tests for `metamoth` package."""

import os

from metamoth import parse_metadata

PACKAGE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(PACKAGE_DIR, "data")
TEST_AUDIO = os.path.join(DATA_DIR, "test.wav")


def test_parse_metadata():
    """Test that metadata can be parsed from WAV file."""
    metadata = parse_metadata(TEST_AUDIO)

    assert metadata.timezone == "UTC"
    assert metadata.audiomoth_id == "0FE081F80FE081F0"
    assert metadata.gain == 2
    assert metadata.battery_state == 4.5
    assert metadata.comment == (
        "Recorded at 19:17:30 06/04/2018 (UTC) by AudioMoth "
        "0FE081F80FE081F0 at gain setting 2 while battery "
        "state was 4.5V"
    )
    assert metadata.samplerate == 192000
    assert metadata.channels == 1
    assert metadata.samples == 3840000
    assert metadata.duration == 20.0


def test_metadata_string_representation_is_comment():
    """Test that metadata string representation is comment."""
    metadata = parse_metadata(TEST_AUDIO)
    assert str(metadata) == metadata.comment
