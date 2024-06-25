"""Test the artist module."""

import os

from metamoth.artist import get_am_artist
from metamoth.chunks import parse_into_chunks

PACKAGE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(PACKAGE_DIR, "data")


def test_get_am_artist_when_missing():
    """Test the get_am_artist function."""
    with open(os.path.join(DATA_DIR, "test.wav"), "rb") as wav:
        riff = parse_into_chunks(wav)
        artist = get_am_artist(wav, riff)
        assert artist is None


def test_get_am_artist():
    """Test the get_am_artist function."""
    with open(os.path.join(DATA_DIR, "test_artist.wav"), "rb") as wav:
        riff = parse_into_chunks(wav)
        artist = get_am_artist(wav, riff)
        assert artist == "243B1F055B2BF663"
