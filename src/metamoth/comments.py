"""Functions for reading the comment chunk of an AudioMoth WAV file."""

from typing import BinaryIO

from metamoth.chunks import Chunk

__all__ = [
    "get_am_comment",
]


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

    Raises
    ------
    ValueError
        If the comment chunk is not found.
    """
    if "LIST" not in chunk.subchunks:
        raise ValueError("No LIST chunk found.")

    sbchunk = chunk.subchunks["LIST"]

    if "ICMT" not in sbchunk.subchunks:
        raise ValueError("No ICMT chunk found.")

    return sbchunk.subchunks["ICMT"]


def get_am_comment(wav: BinaryIO, chunk: Chunk) -> str:
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
    return read_comment(wav, comment_chunk)
