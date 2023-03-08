"""Functions for parsing the comment string of AudioMoth recordings."""
import re
from dataclasses import asdict
from datetime import datetime as dt
from datetime import timedelta as td
from datetime import timezone as tz
from typing import Callable, Dict, Optional, Tuple

from metamoth.enums import FilterType, GainSetting, RecordingState
from metamoth.metadata import (
    AmplitudeThreshold,
    CommentMetadata,
    CommentMetadataV1,
    CommentMetadataV2,
    CommentMetadataV3,
    FrequencyFilter,
)

DATE_FORMAT = "%H:%M:%S %d/%m/%Y"


class MessageFormatError(Exception):
    """Exception raised when the message format is not correct."""


COMMENT_REGEX_1_0 = re.compile(
    r"Recorded at (\d{2}:\d{2}:\d{2} \d{2}\/\d{2}\/\d{4}) by "
    r"AudioMoth ([0-9A-z]{16}) at gain setting (\d) while battery "
    r"state was ([<>]?\s?[0-9\.]*)V"
)


def parse_comment_version_1_0(
    comment: str,
) -> CommentMetadataV1:
    """Parse the comment string of 1.0 firmware.

    Parameters
    ----------
    comment : str
        The comment string.

    Returns
    -------
    metadata : dict

    """
    match = COMMENT_REGEX_1_0.fullmatch(comment)

    if match is None:
        raise MessageFormatError(
            "Comment string does not match expected format."
        )

    low_battery = False
    if match.group(4).startswith("<"):
        low_battery = True
        battery_state_volts = 3.6

    elif match.group(4).startswith(">"):
        battery_state_volts = 5.0

    else:
        battery_state_volts = float(match.group(4))

    return CommentMetadataV1(
        datetime=dt.strptime(match.group(1), DATE_FORMAT),
        timezone=tz(td(0)),
        audiomoth_id=match.group(2),
        gain=GainSetting(int(match.group(3))),
        comment=comment,
        low_battery=low_battery,
        battery_state_v=battery_state_volts,
    )


COMMENT_REGEX_1_0_1 = re.compile(
    r"Recorded at (\d{2}:\d{2}:\d{2} \d{2}\/\d{2}\/\d{4}) \(UTC\) by "
    r"AudioMoth ([0-9A-z]{16}) at gain setting (\d) while battery "
    r"state was ([<>]?\s?[0-9\.]*)V"
)


def parse_comment_version_1_0_1(comment: str) -> CommentMetadataV1:
    """Parse the comment string of 1.0.1 firmware.

    Also valid for version 1.1.0.

    Parameters
    ----------
    comment : str

    Returns
    -------
    metadata: CommentMetadataV1

    """
    match = COMMENT_REGEX_1_0_1.fullmatch(comment)

    if match is None:
        raise MessageFormatError(
            "Comment string does not match expected format."
        )

    low_battery = False
    if match.group(4).startswith("<"):
        low_battery = True
        battery_state_volts = 3.6

    elif match.group(4).startswith(">"):
        battery_state_volts = 5.0

    else:
        battery_state_volts = float(match.group(4))

    return CommentMetadataV1(
        datetime=dt.strptime(match.group(1), DATE_FORMAT),
        timezone=tz(td(0)),
        audiomoth_id=match.group(2),
        gain=GainSetting(int(match.group(3))),
        comment=comment,
        low_battery=low_battery,
        battery_state_v=battery_state_volts,
    )


COMMENT_REGEX_1_2_0 = re.compile(
    r"Recorded at (\d{2}:\d{2}:\d{2} \d{2}\/\d{2}\/\d{4}) \(UTC\) by "
    r"AudioMoth ([0-9A-z]{16}) at gain setting (\d) while battery "
    r"state was ([<>]?\s?[0-9\.]*)V."
)


def parse_comment_version_1_2_0(comment: str) -> CommentMetadataV1:
    """Parse the comment string of 1.2.0 firmware.

    Parameters
    ----------
    comment : str

    Returns
    -------
    metadata: CommentMetadataV1

    """
    match = COMMENT_REGEX_1_2_0.fullmatch(comment)

    if match is None:
        raise MessageFormatError(
            "Comment string does not match expected format."
        )

    low_battery = False
    if match.group(4).startswith("<"):
        low_battery = True
        battery_state_volts = 3.6

    elif match.group(4).startswith(">"):
        battery_state_volts = 5.0

    else:
        battery_state_volts = float(match.group(4))

    return CommentMetadataV1(
        datetime=dt.strptime(match.group(1), DATE_FORMAT),
        timezone=tz(td(0)),
        audiomoth_id=match.group(2),
        gain=GainSetting(int(match.group(3))),
        comment=comment,
        low_battery=low_battery,
        battery_state_v=battery_state_volts,
    )


COMMENT_REGEX_1_2_1 = re.compile(
    r"Recorded at "
    r"(\d{2}:\d{2}:\d{2} \d{2}\/\d{2}\/\d{4}) "  # date time
    r"\(UTC([\+\-]?\d{0,2})\) by "  # timezone
    r"AudioMoth ([0-9A-z]{16}) "  # audiomoth id
    r"at gain setting (\d) while battery state was "  # gain setting
    r"(less than 3\.6|greater than 4\.9|\d\.\d)V"  # battery state
    r"(\. Recording cancelled before completion due to "
    r"(low battery voltage|change of switch position)\.|\.)"
)


def parse_comment_version_1_2_1(comment: str) -> CommentMetadataV2:
    """Parse the comment string of 1.2.1 firmware.

    Parameters
    ----------
    comment : str

    Returns
    -------
    metadata: CommentMetadataV2

    """
    match = COMMENT_REGEX_1_2_1.fullmatch(comment)

    if match is None:
        raise MessageFormatError(
            "Comment string does not match expected format."
        )

    datetime = dt.strptime(match.group(1), DATE_FORMAT)

    if match.group(2) == "":
        timezone = tz(td(0))
    else:
        timezone = tz(td(hours=int(match.group(2))))

    audiomoth_id = match.group(3)

    gain = GainSetting(int(match.group(4)))

    low_battery = False
    if match.group(5) == "less than 3.6":
        low_battery = True
        battery_state_volts = 3.6
    elif match.group(5) == "greater than 4.9":
        battery_state_volts = 5.0
    else:
        battery_state_volts = float(match.group(5))

    recording_state = RecordingState.RECORDING_OKAY
    if match.group(7) == "low battery voltage":
        recording_state = RecordingState.SUPPLY_VOLTAGE_LOW
    elif match.group(7) == "change of switch position":
        recording_state = RecordingState.SWITCH_CHANGED

    return CommentMetadataV2(
        datetime=datetime,
        timezone=timezone,
        audiomoth_id=audiomoth_id,
        gain=gain,
        comment=comment,
        low_battery=low_battery,
        battery_state_v=battery_state_volts,
        recording_state=recording_state,
    )


COMMENT_REGEX_1_2_2 = re.compile(
    r"Recorded at "
    r"(\d{2}:\d{2}:\d{2} \d{2}\/\d{2}\/\d{4}) "  # date time
    r"\(UTC([\+\-]?\d{0,2}:?\d{0,2})\) by "  # timezone
    r"AudioMoth ([0-9A-z]{16}) "  # audiomoth id
    r"at gain setting (\d) while battery state was "  # gain setting
    r"(less than 3\.6|greater than 4\.9|\d\.\d)V"  # battery state
    r"(\. Recording cancelled before completion due to "
    r"(low battery voltage|change of switch position)\.|\.)"
)


def parse_comment_version_1_2_2(comment: str) -> CommentMetadataV2:
    """Parse the comment string of 1.2.2 firmware.

    Also valid for version 1.3.0.

    Parameters
    ----------
    comment : str

    Returns
    -------
    metadata: CommentMetadataV2

    """
    match = COMMENT_REGEX_1_2_2.fullmatch(comment)

    if match is None:
        raise MessageFormatError(
            "Comment string does not match expected format."
        )

    datetime = dt.strptime(match.group(1), DATE_FORMAT)

    if match.group(2) == "":
        timezone = tz(td(0))
    elif ":" not in match.group(2):
        timezone = tz(td(hours=int(match.group(2))))
    else:
        hours, minutes = match.group(2).split(":")
        timezone = tz(td(hours=int(hours), minutes=int(minutes)))

    audiomoth_id = match.group(3)

    gain = GainSetting(int(match.group(4)))

    low_battery = False
    if match.group(5) == "less than 3.6":
        low_battery = True
        battery_state_volts = 3.6
    elif match.group(5) == "greater than 4.9":
        battery_state_volts = 5.0
    else:
        battery_state_volts = float(match.group(5))

    recording_state = RecordingState.RECORDING_OKAY
    if match.group(7) == "low battery voltage":
        recording_state = RecordingState.SUPPLY_VOLTAGE_LOW
    elif match.group(7) == "change of switch position":
        recording_state = RecordingState.SWITCH_CHANGED

    return CommentMetadataV2(
        datetime=datetime,
        timezone=timezone,
        audiomoth_id=audiomoth_id,
        gain=gain,
        comment=comment,
        low_battery=low_battery,
        battery_state_v=battery_state_volts,
        recording_state=recording_state,
    )


COMMENT_REGEX_1_4_0 = re.compile(
    r"Recorded at "
    r"(\d{2}:\d{2}:\d{2} \d{2}\/\d{2}\/\d{4}) "  # date time
    r"\(UTC([\+\-]?\d{0,2}:?\d{0,2})\) by "  # timezone
    r"AudioMoth ([0-9A-z]{16}) "  # audiomoth id
    r"at (low|low-medium|medium|medium-high|high) gain setting "  # gain
    "while battery state was "
    r"(less than 2\.5|greater than 4\.9|\d\.\d)V "  # battery state
    r"and temperature was (-?\d{1,2}\.\d)C."  # temperature
    r"( Amplitude threshold was \d{1,4}\.)?"  # threshold
    r"( Band-pass filter applied with cut-off frequencies of \d{1,4}"
    r"\.\dkHz and \d{1,4}\.\dkHz\.| Low-pass filter applied with cut-off "
    r"frequency of \d{1,4}\.\dkHz\.|"
    r" High-pass filter applied with cut-off frequency of \d{1,4}\.\dkHz\.)?"
    r"( Recording cancelled before completion due to "
    r"(low voltage|change of switch position)\.)?"
)


_gain_mapping = {
    "low": GainSetting.AM_GAIN_LOW,
    "low-medium": GainSetting.AM_GAIN_LOW_MEDIUM,
    "medium": GainSetting.AM_GAIN_MEDIUM,
    "medium-high": GainSetting.AM_GAIN_MEDIUM_HIGH,
    "high": GainSetting.AM_GAIN_HIGH,
}


AMPLITUDE_REGEX = re.compile(r" Amplitude threshold was (\d{1,4})\.")


def _parse_amplitude_threshold_1_4_0(
    comment: Optional[str],
) -> AmplitudeThreshold:
    """Parse the amplitude threshold from the comment string."""
    if comment is None:
        return AmplitudeThreshold(enabled=False, threshold=0)

    match = AMPLITUDE_REGEX.fullmatch(comment)

    if match is None:
        raise MessageFormatError(f"Unexpected amplitude threshold: {comment}")
    return AmplitudeThreshold(enabled=True, threshold=int(match.group(1)))


def _parse_frequency_filter_1_4_0(comment: Optional[str]) -> FrequencyFilter:
    """Parse the frequency filter from the comment string."""
    if comment is None:
        return FrequencyFilter(
            type=FilterType.NO_FILTER,
            lower_frequency_hz=None,
            higher_frequency_hz=None,
        )

    if "Band-pass filter applied" in comment:
        match = re.match(
            r" Band-pass filter applied with cut-off frequencies of "
            r"(\d{1,4}\.\d)kHz and (\d{1,4}\.\d)kHz\.",
            comment,
        )

        if match is None:
            raise MessageFormatError(f"Unexpected frequency filter: {comment}")

        return FrequencyFilter(
            type=FilterType.BAND_PASS,
            lower_frequency_hz=int(float(match.group(1)) * 1000),
            higher_frequency_hz=int(float(match.group(2)) * 1000),
        )

    if "Low-pass filter applied" in comment:
        match = re.match(
            (
                r" Low-pass filter applied with cut-off frequency of "
                r"(\d{1,4}\.\d)kHz\."
            ),
            comment,
        )

        if match is None:
            raise MessageFormatError(f"Unexpected frequency filter: {comment}")

        return FrequencyFilter(
            type=FilterType.LOW_PASS,
            lower_frequency_hz=None,
            higher_frequency_hz=int(float(match.group(1)) * 1000),
        )

    if "High-pass filter applied" in comment:
        match = re.match(
            (
                r" High-pass filter applied with cut-off frequency "
                r"of (\d{1,4}\.\d)kHz\."
            ),
            comment,
        )

        if match is None:
            raise MessageFormatError(f"Unexpected frequency filter: {comment}")

        return FrequencyFilter(
            type=FilterType.HIGH_PASS,
            lower_frequency_hz=int(float(match.group(1)) * 1000),
            higher_frequency_hz=None,
        )

    raise MessageFormatError(f"Unexpected frequency filter: {comment}")


def _parse_timezone(comment: str) -> tz:
    """Parse the timezone from the comment string."""
    if comment == "":
        return tz(td(0))

    if ":" not in comment:
        return tz(td(hours=int(comment)))

    hours, minutes = comment.split(":")
    return tz(td(hours=int(hours), minutes=int(minutes)))


def _parse_recording_state_1_4_0(comment: Optional[str]) -> RecordingState:
    """Parse the recording state from the comment string.

    Works for version 1.4.0 and 1.4.1.
    """
    if comment is None:
        return RecordingState.RECORDING_OKAY

    if "low voltage" in comment:
        return RecordingState.SUPPLY_VOLTAGE_LOW

    if "change of switch position" in comment:
        return RecordingState.SWITCH_CHANGED

    raise MessageFormatError(f"Unexpected recording state: {comment}")


def _parse_battery_state_1_4_0(comment: str) -> Tuple[bool, float]:
    """Parse the battery state from the comment string."""
    low_battery = False
    if comment == "less than 2.5":
        low_battery = True
        battery_state_volts = 2.5
    elif comment == "greater than 4.9":
        battery_state_volts = 5.0
    else:
        battery_state_volts = float(comment)
    return low_battery, battery_state_volts


def parse_comment_version_1_4_0(comment: str) -> CommentMetadataV3:
    """Parse the comment string of 1.4.0 firmware.

    Also valid for version 1.4.1.

    Parameters
    ----------
    comment : str

    Returns
    -------
    metadata: CommentMetadataV3

    """
    match = COMMENT_REGEX_1_4_0.fullmatch(comment)

    if match is None:
        raise MessageFormatError(
            "Comment string does not match expected format."
        )

    datetime = dt.strptime(match.group(1), DATE_FORMAT)
    timezone = _parse_timezone(match.group(2))
    audiomoth_id = match.group(3)
    gain = _gain_mapping[match.group(4)]
    temperature_c = float(match.group(6))
    low_battery, battery_state_volts = _parse_battery_state_1_4_0(
        match.group(5)
    )
    amplitude_threshold = _parse_amplitude_threshold_1_4_0(match.group(7))
    frequency_filter = _parse_frequency_filter_1_4_0(match.group(8))
    recording_state = _parse_recording_state_1_4_0(match.group(9))

    return CommentMetadataV3(
        datetime=datetime,
        timezone=timezone,
        audiomoth_id=audiomoth_id,
        gain=gain,
        comment=comment,
        low_battery=low_battery,
        battery_state_v=battery_state_volts,
        recording_state=recording_state,
        temperature_c=temperature_c,
        amplitude_threshold=amplitude_threshold,
        frequency_filter=frequency_filter,
    )


def _parse_recording_state_1_4_2(comment: Optional[str]) -> RecordingState:
    """Parse the recording state from the comment string of 1.4.2 firmware."""
    if comment is None:
        return RecordingState.RECORDING_OKAY

    if "low voltage" in comment:
        return RecordingState.SUPPLY_VOLTAGE_LOW

    if "file size limit" in comment:
        return RecordingState.FILE_SIZE_LIMITED

    if "change of switch position" in comment:
        return RecordingState.SWITCH_CHANGED

    raise MessageFormatError(f"Unexpected recording state: {comment}")


COMMENT_REGEX_1_4_2 = re.compile(
    r"Recorded at "
    r"(\d{2}:\d{2}:\d{2} \d{2}\/\d{2}\/\d{4}) "  # date time
    r"\(UTC([\+\-]?\d{0,2}:?\d{0,2})\) by "  # timezone
    r"AudioMoth ([0-9A-z]{16}) "  # audiomoth id
    r"at (low|low-medium|medium|medium-high|high) gain setting "  # gain
    "while battery state was "
    r"(less than 2\.5|greater than 4\.9|\d\.\d)V "  # battery state
    r"and temperature was (-?\d{1,2}\.\d)C."  # temperature
    r"( Amplitude threshold was \d{1,4}\.)?"  # threshold
    r"( Band-pass filter applied with cut-off frequencies of \d{1,4}\.\dkHz "
    r"and \d{1,4}\.\dkHz\.| Low-pass filter applied with cut-off frequency of "
    r"\d{1,4}\.\dkHz\."
    r"| High-pass filter applied with cut-off frequency of \d{1,4}\.\dkHz\.)?"
    r"( Recording cancelled before completion due to "
    r"(low voltage|change of switch position|file size limit)\.)?"
)


def parse_comment_version_1_4_2(comment: str) -> CommentMetadataV3:
    """Parse the comment string of 1.4.2 firmware.

    Also valid for version 1.4.3.

    Parameters
    ----------
    comment : str

    Returns
    -------
    metadata: CommentMetadataV3

    """
    match = COMMENT_REGEX_1_4_2.fullmatch(comment)

    if match is None:
        raise MessageFormatError(
            "Comment string does not match expected format."
        )

    datetime = dt.strptime(match.group(1), DATE_FORMAT)
    timezone = _parse_timezone(match.group(2))
    audiomoth_id = match.group(3)
    gain = _gain_mapping[match.group(4)]
    temperature_c = float(match.group(6))
    low_battery, battery_state_volts = _parse_battery_state_1_4_0(
        match.group(5)
    )
    amplitude_threshold = _parse_amplitude_threshold_1_4_0(match.group(7))
    frequency_filter = _parse_frequency_filter_1_4_0(match.group(8))
    recording_state = _parse_recording_state_1_4_2(match.group(9))

    return CommentMetadataV3(
        datetime=datetime,
        timezone=timezone,
        audiomoth_id=audiomoth_id,
        gain=gain,
        comment=comment,
        low_battery=low_battery,
        battery_state_v=battery_state_volts,
        recording_state=recording_state,
        temperature_c=temperature_c,
        amplitude_threshold=amplitude_threshold,
        frequency_filter=frequency_filter,
    )


parsers: Dict[str, Callable[[str], CommentMetadata]] = {
    "1.0": parse_comment_version_1_0,
    "1.0.1": parse_comment_version_1_0_1,
    "1.2.0": parse_comment_version_1_2_0,
    "1.2.1": parse_comment_version_1_2_1,
    "1.2.2": parse_comment_version_1_2_2,
    "1.4.0": parse_comment_version_1_4_0,
    "1.4.2": parse_comment_version_1_4_2,
}


def parse_comment(comment: str) -> dict:
    """Parse the comment string into a dictionary of metadata.

    Parameters
    ----------
    comment : str

    Returns
    -------
    metadata : dict

    """
    for version, parser in parsers.items():
        try:
            return {"firmware_version": version, **asdict(parser(comment))}
        except MessageFormatError:
            continue

    raise MessageFormatError("Comment string does not match any format.")
