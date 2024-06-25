"""Test the chunks module."""

import os

from metamoth.chunks import parse_into_chunks

PACKAGE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(PACKAGE_DIR, "data")
TEST_AUDIO = os.path.join(DATA_DIR, "test.wav")


def test_parses_wavs_into_chunks():
    """Test that WAV file is parsed into chunks."""
    with open(TEST_AUDIO, "rb") as wav:
        chunk = parse_into_chunks(wav)
    assert chunk.chunk_id == "RIFF"
    assert chunk.identifier == "WAVE"
    assert chunk.position == 0
    assert chunk.size == 7680184
    assert len(chunk.subchunks) == 3
    assert chunk.subchunks["fmt "].chunk_id == "fmt "
    assert chunk.subchunks["fmt "].identifier is None
    assert chunk.subchunks["fmt "].position == 12
    assert chunk.subchunks["fmt "].size == 16
    assert chunk.subchunks["fmt "].subchunks == {}
    assert chunk.subchunks["LIST"].chunk_id == "LIST"
    assert chunk.subchunks["LIST"].identifier == "INFO"
    assert chunk.subchunks["LIST"].position == 36
    assert chunk.subchunks["LIST"].size == 140
    assert len(chunk.subchunks["LIST"].subchunks) == 1
    assert chunk.subchunks["LIST"].subchunks["ICMT"].chunk_id == "ICMT"
    assert chunk.subchunks["LIST"].subchunks["ICMT"].size == 128
    assert chunk.subchunks["LIST"].subchunks["ICMT"].identifier is None
    assert chunk.subchunks["LIST"].subchunks["ICMT"].subchunks == {}
    assert chunk.subchunks["data"].chunk_id == "data"
    assert chunk.subchunks["data"].identifier is None
    assert chunk.subchunks["data"].position == 184
    assert chunk.subchunks["data"].size == 7680000
    assert chunk.subchunks["data"].subchunks == {}
