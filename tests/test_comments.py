"""Test comments module."""

import os

import pytest
from metamoth.chunks import parse_into_chunks
from metamoth.comments import get_am_comment

PACKAGE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(PACKAGE_DIR, "data")
TEST_AUDIO = os.path.join(DATA_DIR, "test.wav")
TEST_COMMENT = (
    "Recorded at 19:17:30 06/04/2018 (UTC) by AudioMoth "
    "0FE081F80FE081F0 at gain setting 2 while battery "
    "state was 4.5V"
)


def test_get_comment_from_wav_file():
    """Test that comment can be extracted from WAV file."""
    with open(TEST_AUDIO, "rb") as wav:
        chunk = parse_into_chunks(wav)
        comment = get_am_comment(wav, chunk)

    assert comment == TEST_COMMENT


def test_get_comment_fails_for_non_audiomoth_file():
    """Test that comment cannot be extracted from non-AudioMoth WAV file."""
    with pytest.raises(ValueError):
        with open(os.path.join(DATA_DIR, "non_am.wav"), "rb") as wav:
            chunk = parse_into_chunks(wav)
            get_am_comment(wav, chunk)
