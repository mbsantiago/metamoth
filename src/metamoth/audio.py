"""Audio file utilities."""

import os
from typing import Union

PathLike = Union[os.PathLike, str]  # pylint: disable=no-member


def is_wav_filename(filename: PathLike) -> bool:
    """Return True if filename is a WAV file."""
    filename = str(filename)
    return filename.endswith(".wav") or filename.endswith(".WAV")


def is_riff(path: PathLike) -> bool:
    """Return True if path is a RIFF file.

    An RIFF file is a IFF file with the RIFF chunk ID. The RIFF chunk ID
    is the first 4 bytes of the file.

    Parameters
    ----------
    path : PathLike

    Returns
    -------
    bool
    """
    with open(path, "rb") as riff:
        return riff.read(4) == b"RIFF"


def is_wav(path: PathLike) -> bool:
    """Return True if path is a WAV file.

    A WAV file is a RIFF file with the WAVE chunk ID. The WAVE chunk ID
    is the 8th byte of the file.

    Parameters
    ----------
    path : PathLike

    Returns
    -------
    bool
    """
    with open(path, "rb") as wav:
        if wav.read(4) != b"RIFF":
            return False

        wav.seek(8)
        return wav.read(4) == b"WAVE"
