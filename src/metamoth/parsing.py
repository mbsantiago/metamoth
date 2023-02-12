"""Functions for parsing the comment string of AudioMoth recordings."""
import re
from dataclasses import asdict
from datetime import datetime as dt
from datetime import timedelta as td
from datetime import timezone as tz
from typing import Callable, Dict

from metamoth.enums import GainSetting, RecordingState
from metamoth.metadata import (
    CommentMetadata,
    CommentMetadataV1,
    CommentMetadataV2,
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
    r"\(UTC([\+\-]?\d{0,2}):?\d{0,2}\) by "  # timezone
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


parsers: Dict[str, Callable[[str], CommentMetadata]] = {
    "1.0": parse_comment_version_1_0,
    "1.0.1": parse_comment_version_1_0_1,
    "1.2.0": parse_comment_version_1_2_0,
    "1.2.1": parse_comment_version_1_2_1,
    "1.2.2": parse_comment_version_1_2_2,
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
