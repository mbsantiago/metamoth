"""Main module."""
import os
from typing import Union

from metamoth.chunks import parse_into_chunks
from metamoth.comments import get_comments
from metamoth.mediainfo import get_media_info
from metamoth.metadata import AMMetadataV1

__all__ = [
    "parse_metadata",
]


PathLike = Union[os.PathLike, str]


def parse_metadata(path: PathLike) -> AMMetadataV1:
    """Parse the metadata from an AudioMoth recording.

    Parameters
    ----------
    path : PathLike

    Returns
    -------
    Metadata
    """
    with open(path, "rb") as wav:
        riff = parse_into_chunks(wav)
        media_info = get_media_info(wav, riff)
        metadata = get_comments(wav, riff)

    return AMMetadataV1(
        path=str(path),
        samplerate=media_info.samplerate,
        duration=media_info.duration,
        samples=media_info.samples,
        channels=media_info.channels,
        datetime=metadata.datetime,
        timezone=metadata.timezone,
        audiomoth_id=metadata.audiomoth_id,
        gain=metadata.gain,
        battery_state=metadata.battery_state,
        comment=metadata.comment,
        firmware_version="1.1.0",
    )
