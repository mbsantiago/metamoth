"""Module with AM Metadata structure for different firmware versions.

This module contains the AMMetadata class and its subclasses for different
firmware versions.
"""

# pylint: disable=too-many-instance-attributes
from dataclasses import dataclass
from datetime import datetime as dt
from datetime import timezone as tz
from typing import Optional

from metamoth.enums import FilterType, GainSetting, RecordingState
from metamoth.mediainfo import MediaInfo

__all__ = [
    "CommentMetadata",
    "CommentMetadataV1",
    "CommentMetadataV2",
    "CommentMetadataV3",
    "CommentMetadataV4",
    "CommentMetadataV5",
    "CommentMetadataV6",
    "AMMetadata",
    "FrequencyFilter",
    "AmplitudeThreshold",
    "FrequencyTrigger",
    "ExtraMetadata",
    "assemble_metadata",
]


@dataclass
class FrequencyFilter:
    """Frequency filter applied to the recording."""

    type: FilterType
    """Filter type applied to the recording."""

    higher_frequency_hz: Optional[int]
    """Higher filter frequency in Hz. None if no upper filter is applied."""

    lower_frequency_hz: Optional[int]
    """Lower filter frequency in Hz. None if no lower filter is applied."""


@dataclass
class AmplitudeThreshold:
    """Amplitude threshold applied to the recording."""

    enabled: bool
    """True if the amplitude threshold is enabled."""

    threshold: int
    """Amplitude threshold."""


@dataclass
class FrequencyTrigger:
    """Frequency trigger metadata."""

    enabled: bool
    """True if frequency trigger is enabled."""

    centre_frequency_hz: int
    """Centre frequency in Hz."""

    window_length_shift: int
    """Window length shift in samples."""


@dataclass
class CommentMetadata:
    """Base class for AudioMoth metadata stored in comment."""

    audiomoth_id: str
    """AudioMoth ID. This is the serial number of the AudioMoth."""

    datetime: dt
    """Datetime of the recording."""

    timezone: tz
    """Timezone of the recording."""

    gain: GainSetting
    """Gain setting of the AudioMoth."""

    comment: str
    """Full comment string."""

    low_battery: bool
    """True if the battery is low."""

    battery_state_v: float
    """Battery state in volts."""


@dataclass
class CommentMetadataV1(CommentMetadata):
    """AudioMoth recording metadata in comment string.

    Valid for versions 1.0, 1.0.1, 1.1.0, 1.2.0,

    Timezone is always UTC for versions 1.0 and 1.0.1. For versions 1.1.0 and
    1.2.0, the an UTC hour offset can be set in the AudioMoth settings.
    """


@dataclass
class CommentMetadataV2(CommentMetadata):
    """AudioMoth recording metadata in comment string.

    Valid for versions 1.2.1, 1.2.2, 1.3.0
    """

    recording_state: RecordingState
    """Recording state of the AudioMoth."""


@dataclass
class CommentMetadataV3(CommentMetadata):
    """AudioMoth recording metadata in comment string.

    Valid for versions 1.4.0, 1.4.1, 1.4.2, 1.4.3, 1.4.4
    """

    recording_state: RecordingState
    """Recording state of the AudioMoth."""

    temperature_c: float
    """Temperature in degrees Celsius."""

    amplitude_threshold: AmplitudeThreshold
    """Amplitude threshold applied to the recording."""

    frequency_filter: FrequencyFilter
    """Frequency filter applied to the recording."""


@dataclass
class CommentMetadataV4(CommentMetadata):
    """AudioMoth recording metadata in comment string.

    Valid for version 1.5.0
    """

    recording_state: RecordingState
    """Recording state of the AudioMoth."""

    temperature_c: float
    """Temperature in degrees Celsius."""

    amplitude_threshold: AmplitudeThreshold
    """Amplitude threshold applied to the recording."""

    frequency_filter: FrequencyFilter
    """Frequency filter applied to the recording."""

    deployment_id: Optional[int]
    """Deployment ID of the AudioMoth."""

    external_microphone: bool
    """True if an external microphone is connected to the AudioMoth."""


@dataclass
class CommentMetadataV5(CommentMetadata):
    """AudioMoth recording metadata in comment string.

    Valid for versions 1.6.0, 1.7.0 and 1.7.1
    """

    recording_state: RecordingState
    """Recording state of the AudioMoth."""

    temperature_c: float
    """Temperature in degrees Celsius."""

    amplitude_threshold: AmplitudeThreshold
    """Amplitude threshold applied to the recording."""

    frequency_filter: FrequencyFilter
    """Frequency filter applied to the recording."""

    deployment_id: Optional[str]
    """Deployment ID of the AudioMoth."""

    external_microphone: bool
    """True if an external microphone is connected to the AudioMoth."""

    minimum_trigger_duration_s: int
    """Minimum trigger duration in seconds."""


@dataclass
class CommentMetadataV6(CommentMetadata):
    """AudioMoth recording metadata in comment string.

    Valid for versions 1.8.0 and 1.8.1
    """

    recording_state: Optional[RecordingState] = RecordingState.RECORDING_OKAY
    """Recording state of the AudioMoth."""

    temperature_c: Optional[float] = None
    """Temperature in degrees Celsius."""

    amplitude_threshold: Optional[AmplitudeThreshold] = None
    """Amplitude threshold applied to the recording."""

    frequency_filter: Optional[FrequencyFilter] = None
    """Frequency filter applied to the recording."""

    deployment_id: Optional[int] = None
    """Deployment ID of the AudioMoth."""

    external_microphone: bool = False
    """True if an external microphone is connected to the AudioMoth."""

    minimum_trigger_duration_s: Optional[int] = None
    """Minimum trigger duration in seconds."""

    frequency_trigger: Optional[FrequencyTrigger] = None
    """Frequency trigger metadata."""


@dataclass
class ExtraMetadata:
    """Extra metadata."""

    path: str
    """Path to the recording."""

    firmware_version: str
    """Firmware version of the AudioMoth."""


@dataclass
class AMMetadata(CommentMetadataV6, MediaInfo, ExtraMetadata):
    """AudioMoth recording metadata."""


def assemble_metadata(
    path: str,
    media_info: MediaInfo,
    comment_metadata: dict,
    artist: Optional[str],
) -> AMMetadata:
    """Assemble the metadata for the recording.

    Parameters
    ----------
    media_info : dict
        Media information dictionary.

    metadata : dict
        Metadata dictionary.

    artist : str
        Artist string. Can be None.

    Returns
    -------
    metadata : AMMetadataV6
        Metadata object.

    """
    if comment_metadata["audiomoth_id"] is None:
        if artist is None:
            raise ValueError("No AudioMoth ID found in comment or artist.")

        comment_metadata["audiomoth_id"] = artist

    return AMMetadata(
        path=path,
        samplerate_hz=media_info.samplerate_hz,
        duration_s=media_info.duration_s,
        samples=media_info.samples,
        channels=media_info.channels,
        **comment_metadata,
    )
