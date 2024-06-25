"""Get media information from a WAV file.

The WAV file must be a PCM WAV file. The WAV file must have a fmt chunk
and a data chunk. The WAV file must have a samplerate and channels
information in the fmt chunk.
"""

from dataclasses import dataclass
from typing import BinaryIO, Tuple

from metamoth.chunks import Chunk

__all__ = [
    "MediaInfo",
    "get_media_info",
]


@dataclass
class MediaInfo:
    """Media information."""

    samplerate_hz: int
    """Sample rate in Hz."""

    duration_s: float
    """Duration in seconds."""

    samples: int
    """Number of samples."""

    channels: int
    """Number of channels."""


def read_samplerate_and_channels(
    wav: BinaryIO,
    fmt_chunk: Chunk,
) -> Tuple[int, int]:
    """Return the media information from the fmt chunk.

    Parameters
    ----------
    wav : BinaryIO
        Open file object of the WAV file.

    chunk : Chunk
        The fmt chunk info.

    Returns
    -------
    samplerate : int
    channels: int
    """
    wav.seek(fmt_chunk.position + 8)
    wav.read(2)  # audio format
    channels = int.from_bytes(wav.read(2), "little")
    samplerate = int.from_bytes(wav.read(4), "little")
    return samplerate, channels


def get_media_info(wav: BinaryIO, chunk: Chunk) -> MediaInfo:
    """Return the media information from the WAV file.

    Parameters
    ----------
    wav : BinaryIO
        Open file object of the WAV file.

    chunk : Chunk
        The RIFF chunk info, which is the root chunk. Should include
        the fmt and data chunks as subchunks.

    Returns
    -------
    MediaInfo
    """
    fmt_chunk = chunk.subchunks["fmt "]
    data_chunk = chunk.subchunks["data"]
    samplerate, channels = read_samplerate_and_channels(wav, fmt_chunk)
    samples = data_chunk.size // (channels * 2)
    duration = samples / samplerate
    return MediaInfo(
        samplerate_hz=samplerate,
        channels=channels,
        samples=samples,
        duration_s=duration,
    )
