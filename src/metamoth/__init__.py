"""Metamoth: A Python package for parsing AudioMoth metadata.

Metamoth is a Python package for parsing metadata from AudioMoth recordings. It
provides a function to parse the metadata from a WAV file and returns an
object with the metadata as attributes.
"""

from metamoth.metamoth import parse_metadata

__author__ = """Santiago Martinez Balvanera"""
__email__ = "santiago.balvanera.20@ucl.ac.uk"
__version__ = "1.2.2"


__all__ = ["parse_metadata"]
