"""Test comments module."""
import datetime
import os

from metamoth.chunks import parse_into_chunks
from metamoth.comments import get_comments, parse_comment

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
