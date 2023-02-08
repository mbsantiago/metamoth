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
    assert chunk.subchunks[0].chunk_id == "fmt "
    assert chunk.subchunks[0].identifier is None
    assert chunk.subchunks[0].position == 12
    assert chunk.subchunks[0].size == 16
    assert chunk.subchunks[0].subchunks == []
    assert chunk.subchunks[1].chunk_id == "LIST"
    assert chunk.subchunks[1].identifier == "INFO"
    assert chunk.subchunks[1].position == 36
    assert chunk.subchunks[1].size == 140
    assert len(chunk.subchunks[1].subchunks) == 1
    assert chunk.subchunks[1].subchunks[0].chunk_id == "ICMT"
    assert chunk.subchunks[1].subchunks[0].size == 128
    assert chunk.subchunks[1].subchunks[0].identifier is None
    assert chunk.subchunks[1].subchunks[0].subchunks == []
    assert chunk.subchunks[2].chunk_id == "data"
    assert chunk.subchunks[2].identifier is None
    assert chunk.subchunks[2].position == 184
    assert chunk.subchunks[2].size == 7680000
    assert chunk.subchunks[2].subchunks == []
