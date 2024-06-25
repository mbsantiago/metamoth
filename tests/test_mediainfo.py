"""Test the media info module."""

import os
import wave

from metamoth.chunks import parse_into_chunks
from metamoth.mediainfo import get_media_info

PACKAGE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(PACKAGE_DIR, "data")
TEST_AUDIO = os.path.join(DATA_DIR, "test.wav")


def test_get_media_info():
    """Test that media info can be parsed from WAV file."""
    with open(TEST_AUDIO, "rb") as wav:
        chunk = parse_into_chunks(wav)
        media_info = get_media_info(wav, chunk)

    with wave.open(TEST_AUDIO, "rb") as wav:
        assert media_info.samplerate_hz == wav.getframerate()
        assert media_info.channels == wav.getnchannels()
        assert media_info.samples == wav.getnframes()
        assert media_info.duration_s == wav.getnframes() / wav.getframerate()
