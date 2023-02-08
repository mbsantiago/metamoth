"""Parse the comment string into a tuple of metadata.

This module is based on the AudioMoth comment format:

    Recorded at 19:17:30 06/04/2018 (UTC) by AudioMoth 0FE081F80FE081F0
    at gain setting 2 while battery state was 4.5V

"""

import datetime
import re
from collections import namedtuple
from typing import BinaryIO

from metamoth.chunks import Chunk

__all__ = [
    "AudioMothComment",
    "parse_comment",
]

COMMENT_REGEX = re.compile(
    r"Recorded at (\d{2}:\d{2}:\d{2} \d{2}\/\d{2}\/\d{4}) \((UTC[^\)]*)\) by "
    r"AudioMoth ([0-9A-z]{16}) at gain setting (\d) while battery "
    r"state was ([0-9\.]*)V"
)


DATE_FORMAT = "%H:%M:%S %d/%m/%Y"


AudioMothComment = namedtuple(
    "AudioMothComment",
    [
        "datetime",
        "timezone",
        "audiomoth_id",
        "gain",
        "battery_state",
        "comment",
    ],
)


def parse_comment(comment: str) -> AudioMothComment:
    """Parse the comment string into a tuple of metadata.

    Parameters
    ----------
    comment : str
        The comment string.

    Returns
    -------
    datetime : datetime.datetime
        The datetime of the recording.

    timezone:
        The timezone of the recording.

    audiomoth_id : str
        The ID of the AudioMoth.

    gain : int
        The gain setting of the AudioMoth.

    battery_state : float
        State of the battery in volts at time of recording.

    """
    match = COMMENT_REGEX.match(comment)
    if match is None:
        raise ValueError("Comment string does not match expected format.")

    return AudioMothComment(
        datetime.datetime.strptime(match.group(1), DATE_FORMAT),
        match.group(2),
        match.group(3),
        int(match.group(4)),
        float(match.group(5)),
        comment,
    )


def read_comment(wav: BinaryIO, comment_chunk: Chunk) -> str:
    """Return the comment from the comment chunk.

    Parameters
    ----------
    wav : BinaryIO
        Open file object of the WAV file.

    chunk : Chunk
        The comment chunk info.

    Returns
    -------
    comment : str
    """
    wav.seek(comment_chunk.position + 8)
    comment = wav.read(comment_chunk.size - 4).decode("utf-8").strip("\x00")
    return comment


def get_comment_chunk(chunk: Chunk) -> Chunk:
    """Return the comment chunk from the RIFF chunk.

    Parameters
    ----------
    chunk : Chunk
        The RIFF chunk info, which is the root chunk.

    Returns
    -------
    comment_chunk : Chunk
    """
    for subchunk in chunk.subchunks:
        if subchunk.chunk_id == "LIST":
            break
    else:
        raise ValueError("No LIST chunk found.")

    for subsubchunk in subchunk.subchunks:
        if subsubchunk.chunk_id == "ICMT":
            return subsubchunk

    raise ValueError("No comment chunk found.")


def get_comments(wav: BinaryIO, chunk: Chunk) -> AudioMothComment:
    """Return the comment from the WAV file.

    Parameters
    ----------
    wav : BinaryIO
        Open file object of the WAV file.

    chunk : Chunk
        The RIFF chunk info, which is the root chunk. Should include
        the LIST chunk as a subchunk.

    Returns
    -------
    comment : str
    """
    comment_chunk = get_comment_chunk(chunk)
    comment = read_comment(wav, comment_chunk)
    return parse_comment(comment)
