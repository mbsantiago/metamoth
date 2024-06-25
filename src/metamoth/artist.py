"""Functions for reading the artist chunk from a WAV file."""

from typing import BinaryIO, Optional

from metamoth.chunks import Chunk

__all__ = [
    "get_am_artist",
]


def read_artist(wav: BinaryIO, artist_chunk: Chunk) -> str:
    """Return the artist from the artist chunk.

    Parameters
    ----------
    wav : BinaryIO
        Open file object of the WAV file.

    artist_chunk : Chunk
        The artist chunk

    Returns
    -------
    artist: str
    """
    wav.seek(artist_chunk.position + 8)
    comment = wav.read(artist_chunk.size - 4).decode("utf-8").strip("\x00")
    return comment


def get_artist_chunk(chunk: Chunk) -> Optional[Chunk]:
    """Get the artist chunk from the RIFF chunk.

    Parameters
    ----------
    chunk : Chunk
        The RIFF chunk, which is the root chunk.

    Returns
    -------
    Chunk
        The artist chunk. If the chunk is not found, returns None.
    """
    list_chunk = chunk.subchunks.get("LIST")

    if list_chunk is None:
        return None

    return list_chunk.subchunks.get("IART")


def get_audiomoth_id_from_artist(comment: str) -> str:
    """Get the AudioMoth ID from the artist string.

    Parameters
    ----------
    comment : str
        The artist string.

    Returns
    -------
    str
        The AudioMoth ID.
    """
    return comment.split(" ")[-1]


def get_am_artist(wav: BinaryIO, chunk: Chunk) -> Optional[str]:
    """Get the artist string from the WAV file.

    Parameters
    ----------
    wav : BinaryIO
        The WAV file.

    chunk : Chunk
        The RIFF chunk, which is the root chunk.

    Returns
    -------
    str
        The artist string. If the artist is not found, returns None.
    """
    artist_chunk = get_artist_chunk(chunk)

    if artist_chunk is None:
        return None

    artist = read_artist(wav, artist_chunk)
    return get_audiomoth_id_from_artist(artist)
