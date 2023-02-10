"""Module with AM Metadata structure for different firmware versions."""
# pylint: disable=too-many-instance-attributes
from dataclasses import dataclass
from datetime import datetime as dt
from datetime import timezone as tz
from typing import Optional

from metamoth.enums import (
    BatteryState,
    ExtendedBatteryState,
    FilterType,
    GainSetting,
    RecordingState,
)

__all__ = [
    "AMMetadata",
    "AMMetadataV1",
    "AMMetadataV2",
    "AMMetadataV3",
    "AMMetadataV4",
    "AMMetadataV5",
    "AMMetadataV6",
]


@dataclass
class AMMetadata:
    """Base class for AudioMoth metadata."""

    path: str
    """Path to the recording."""

    samplerate: int
    """Sample rate in Hz."""

    duration: float
    """Duration in seconds."""

    samples: int
    """Number of samples."""

    channels: int
    """Number of channels."""

    audiomoth_id: str
    """AudioMoth ID. This is the serial number of the AudioMoth."""

    datetime: dt
    """Datetime of the recording."""

    gain: GainSetting
    """Gain setting of the AudioMoth."""

    comment: str
    """Full comment string."""

    timezone: tz
    """Timezone of the recording."""

    firmware_version: str
    """Firmware version of the AudioMoth."""

    def __str__(self):
        """Return a string representation of the metadata."""
        return self.comment


@dataclass
class AMMetadataV1(AMMetadata):
    """AudioMoth recording metadata.

    Valid for versions 1.0, 1.0.1, 1.1.0, 1.2.0,

    Timezone is always UTC for versions 1.0 and 1.0.1. For versions 1.1.0 and
    1.2.0, the an UTC hour offset can be set in the AudioMoth settings.
    """

    battery_state: BatteryState
    """Battery state of the AudioMoth."""


@dataclass
class AMMetadataV2(AMMetadata):
    """AudioMoth recording metadata.

    Valid for versions 1.2.1, 1.2.2, 1.3.0
    """

    battery_state: BatteryState
    """Battery state of the AudioMoth."""

    recording_state: RecordingState
    """Recording state of the AudioMoth."""


@dataclass
class FrequencyFilter:
    """Frequency filter applied to the recording."""

    type: FilterType
    """Filter type applied to the recording."""

    higher_frequency: Optional[int]
    """Higher filter frequency in Hz. None if no upper filter is applied."""

    lower_frequency: Optional[int]
    """Lower filter frequency in Hz. None if no lower filter is applied."""


@dataclass
class AmplitudeThreshold:
    """Amplitude threshold applied to the recording."""

    enabled: bool
    """True if the amplitude threshold is enabled."""

    threshold: int
    """Amplitude threshold in dB."""


@dataclass
class AMMetadataV3(AMMetadata):
    """AudioMoth recording metadata.

    Valid for versions 1.4.0, 1.4.1, 1.4.2, 1.4.3, 1.4.4
    """

    battery_state: ExtendedBatteryState
    """Battery state of the AudioMoth. This is the extended battery state."""

    recording_state: RecordingState
    """Recording state of the AudioMoth."""

    temperature: float
    """Temperature in degrees Celsius."""

    amplitude_threshold: AmplitudeThreshold
    """Amplitude threshold applied to the recording."""

    frequency_filter: FrequencyFilter
    """Frequency filter applied to the recording."""


@dataclass
class AMMetadataV4(AMMetadata):
    """AudioMoth recording metadata.

    Valid for version 1.5.0
    """

    battery_state: ExtendedBatteryState
    """Battery state of the AudioMoth. This is the extended battery state."""

    recording_state: RecordingState
    """Recording state of the AudioMoth."""

    temperature: float
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
class AMMetadataV5(AMMetadata):
    """AudioMoth recording metadata.

    Valid for versions 1.6.0, 1.7.0 and 1.7.1
    """

    battery_state: ExtendedBatteryState
    """Battery state of the AudioMoth. This is the extended battery state."""

    recording_state: RecordingState
    """Recording state of the AudioMoth."""

    temperature: float
    """Temperature in degrees Celsius."""

    amplitude_threshold: AmplitudeThreshold
    """Amplitude threshold applied to the recording."""

    frequency_filter: FrequencyFilter
    """Frequency filter applied to the recording."""

    deployment_id: Optional[int]
    """Deployment ID of the AudioMoth."""

    external_microphone: bool
    """True if an external microphone is connected to the AudioMoth."""

    minimum_trigger_duration: int
    """Minimum trigger duration in seconds."""


@dataclass
class FrequencyTrigger:
    """Frequency trigger metadata."""

    enabled: bool
    """True if frequency trigger is enabled."""

    centre_frequency: int
    """Centre frequency in Hz."""

    window_length_shift: int
    """Window length shift in samples."""


@dataclass
class AMMetadataV6(AMMetadata):
    """AudioMoth recording metadata.

    Valid for versions 1.8.0 and 1.8.1
    """

    battery_state: ExtendedBatteryState
    """Battery state of the AudioMoth. This is the extended battery state."""

    recording_state: RecordingState
    """Recording state of the AudioMoth."""

    temperature: float
    """Temperature in degrees Celsius."""

    amplitude_threshold: AmplitudeThreshold
    """Amplitude threshold applied to the recording."""

    frequency_filter: FrequencyFilter
    """Frequency filter applied to the recording."""

    deployment_id: Optional[int]
    """Deployment ID of the AudioMoth."""

    external_microphone: bool
    """True if an external microphone is connected to the AudioMoth."""

    minimum_trigger_duration: int
    """Minimum trigger duration in seconds."""

    frequency_trigger: FrequencyTrigger
    """Frequency trigger metadata."""
