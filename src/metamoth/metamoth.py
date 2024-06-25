"""Main module."""

import os
from typing import Union

from metamoth.artist import get_am_artist
from metamoth.chunks import parse_into_chunks
from metamoth.comments import get_am_comment
from metamoth.mediainfo import get_media_info
from metamoth.metadata import AMMetadata, assemble_metadata
from metamoth.parsing import parse_comment

__all__ = [
    "parse_metadata",
]


PathLike = Union[os.PathLike, str]  # pylint: disable=no-member


def parse_metadata(path: PathLike) -> AMMetadata:
    """Parse the metadata from an AudioMoth recording.

    Parameters
    ----------
    path : PathLike

    Returns
    -------
    Metadata
        Parse metadata from the recording at `path`. The metadata is
        returned as a :py:class:`AMMetadata` object.
    """
    with open(path, "rb") as wav:
        riff = parse_into_chunks(wav)
        media_info = get_media_info(wav, riff)
        comment = get_am_comment(wav, riff)
        artist = get_am_artist(wav, riff)

    am_metadata = parse_comment(comment)
    return assemble_metadata(str(path), media_info, am_metadata, artist)
