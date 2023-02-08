"""Main module."""
import datetime
import os
from dataclasses import dataclass
from typing import Union

from metamoth.chunks import parse_into_chunks
from metamoth.comments import get_comments
from metamoth.mediainfo import get_media_info

__all__ = [
    "Metadata",
    "parse_metadata",
]


PathLike = Union[os.PathLike, str]


@dataclass
class Metadata:
    """AudioMoth recording metadata.

    Parameters
    ----------
    path: str

    samplerate : int

    duration : float

    samples : int

    channels : int

    datetime : datetime.datetime

    timezone : str

    audiomoth_id : str

    gain : int

    battery_state : float

    comment : str
    """

    # pylint: disable=too-many-instance-attributes

    path: str
    samplerate: int
    duration: float
    samples: int
    channels: int
    datetime: datetime.datetime
    timezone: str
    audiomoth_id: str
    gain: int
    battery_state: float
    comment: str

    def __str__(self):
        """Return a string representation of the metadata."""
        return (
            f"AudioMoth recording at {self.datetime} ({self.timezone}) "
            f"with ID {self.audiomoth_id} at gain setting {self.gain} "
            f"while battery state was {self.battery_state}V."
        )

    def __repr__(self):
        """Return a string representation of the metadata."""
        return (
            f"Metadata(path={self.path}, samplerate={self.samplerate}, "
            f"duration={self.duration}, samples={self.samples}, "
            f"channels={self.channels}, datetime={self.datetime}, "
            f"timezone={self.timezone}, audiomoth_id={self.audiomoth_id}, "
            f"gain={self.gain}, battery_state={self.battery_state})"
        )


def parse_metadata(path: PathLike) -> Metadata:
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

    return Metadata(
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
    )
