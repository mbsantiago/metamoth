"""Test audio module"""

import os

from metamoth.audio import is_riff, is_wav, is_wav_filename

PACKAGE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(PACKAGE_DIR, "data")
TEST_AUDIO = os.path.join(DATA_DIR, "test.wav")


def test_audio_exists():
    """Test that test audio file exists."""
    assert os.path.exists(TEST_AUDIO)


def test_is_wav_filename():
    """Test that test audio file is a WAV file."""
    assert is_wav_filename(TEST_AUDIO)


def test_is_riff():
    """Test that test audio file is a RIFF file."""
    assert is_riff(TEST_AUDIO)


def test_is_wav():
    """Test that test audio file is a WAV file."""
    assert is_wav(TEST_AUDIO)
