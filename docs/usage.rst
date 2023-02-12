=====
Usage
=====

Simple example
==============

The ``metamoth`` package provides a single function, ``parse_metadata``,
which parses the metadata of an AudioMoth file and returns an object
containing the metadata.

.. code-block:: python

    from metamoth import parse_metadata

    metadata = parse_metadata('path/to/file')

The extracted metadata can be accessed as attributes of the object, as shown

.. code-block:: python

    duration = metadata.duration_s
    path = metadata.path
    # etc.

Metadata
========

The ``metadata`` variable is an object (of type
:py:class:`metamoth.metadata.AMMetadata`) containing the metadata of the file.

The extracted metadata contains:

* ``path``: the path of the audio file
* ``firmware_version``: the firmware version of the AudioMoth that
  recorded the file. Since the AudioMoth firmware version is not stored in the
  recording, this is an estimate and may be incorrect.

Media Information
-----------------

* ``duration_s``: the duration of the file in seconds.
* ``samplerate_hz``: the sample rate of the file in Hz.
* ``channels``: the number of channels in the file.
* ``samples``: the number of audio samples in the file.

AudioMoth Information
---------------------

Data extracted from the AudioMoth comment string:

* ``datetime``: the date and time of the file in a datetime_ object.
* ``timezone``: the timezone of the file as a timezone_ object.
* ``audiomoth_id``: the ID of the AudioMoth that recorded the file.
* ``battery_state_v``: the battery state of the AudioMoth that recorded
  the file in Volts.
* ``low_battery``: a boolean indicating if the battery state is low.
* ``gain``: the gain setting of the AudioMoth that recorded the file.
* ``comment``: the full comment string in the WAV header.

The following fields are only available for some AudioMoth firmware versions.
Nonetheless, they are always present in the metadata object, but may be
``None``.

* ``recording_state``: the :ref:`recording state` of the AudioMoth that
  recorded the file.
* ``temperature_c``: the temperature of the AudioMoth in Celsius.
* ``amplitude_threshold``: information concerning the whether an
  :ref:`amplitude threshold` was used and the threshold value.
* ``frequency_filter``: information concerning the whether a :ref:`frequency
  filter` was used and the filter settings.
* ``deployment_id``: the deployment ID as set by the user.
* ``external_microphone``: a boolean indicating if an external microphone was
  used.
* ``minimum_trigger_duration_s``: the minimum trigger duration in seconds.
* ``frequency_trigger``: information concerning the whether a :ref:`frequency
  trigger` was used and the trigger settings.

.. _recording state:

Recording State
---------------

The recording state is an object (of type
:py:class:`metamoth.enums.RecordingState`) indicating the state of the
AudioMoth when the recording was made. It can be one of the following:

* ``RECORDING_OKAY``: the AudioMoth was recording normally.
* ``FILE_SIZE_LIMITED``: The AudioMoth stopped recording because
  the file size limit was reached.
* ``SUPPLY_VOLTAGE_LOW``: The AudioMoth stopped recording
  because the battery was low.
* ``SWITCH_CHANGED``: The AudioMoth stopped recording because
  the switch was changed.
* ``MICROPHONE_CHANGED``: The AudioMoth stopped recording
  because the microphone was changed.
* ``MAGNETIC_SWITCH``: The AudioMoth stopped recording because
  the magnetic switch was triggered.
* ``SDCARD_WRITE_ERROR``: The AudioMoth stopped recording
  because of an error writing to the SD card.

.. _amplitude threshold:

Amplitude Threshold
-------------------

The amplitude threshold is an object (of type
:py:class:`metamoth.metadata.AmplitudeThreshold`) that holds information
about the amplitude threshold used to trigger the recording. It has the
following attributes:

* ``enabled``: a boolean indicating if an amplitude threshold was used.
* ``threshold``: the amplitude threshold in dB.

.. _frequency filter:

Frequency Filter
----------------

The frequency filter is an object (of type
:py:class:`metamoth.metadata.FrequencyFilter`) that holds information about the
frequency filters used on the recording. It has the following attributes:

* ``type``: the type of the filter as a :py:class:`metamoth.enums.FilterType`
  object. It can be one of the following

    - ``LOW_PASS``
    - ``HIGH_PASS``
    - ``NO_FILTER``
    - ``BAND_PASS``

* ``lower_frequency_hz``: the lower frequency of the filter in Hz. If the
  filter is a high-pass filter, this will be ``None``.
* ``higher_frequency_hz``: the upper frequency of the filter in Hz. If the
  filter is a low-pass filter, this will be ``None``.

.. _frequency trigger:

Frequency Trigger
-----------------

The frequency trigger is an object (of type :py:class:`metamoth.metadata.FrequencyTrigger`)
that holds information about the frequency trigger used to trigger the
recording. It has the following attributes:

* ``enabled``: a boolean indicating if a frequency trigger was used.
* ``centre_frequency_hz``: the centre frequency of the trigger in Hz.
* ``window_length_shift``: the window length shift in samples of the trigger.

.. _AudioMoth firmware versions:

Fields available for each AudioMoth firmware
--------------------------------------------

The following table shows the fields available for each AudioMoth firmware.

+---------+-----------------+---------------+---------------------+------------------+---------------+---------------------+----------------------------+-------------------+
| version | recording_state | temperature_c | amplitude_threshold | frequency_filter | deployment_id | external_microphone | minimum_trigger_duration_s | frequency_trigger |
+=========+=================+===============+=====================+==================+===============+=====================+============================+===================+
|   1.0   |        ✖        |       ✖       |          ✖          |        ✖         |       ✖       |          ✖          |             ✖              |         ✖         |
+---------+-----------------+---------------+---------------------+------------------+---------------+---------------------+----------------------------+-------------------+
|  1.0.1  |        ✖        |       ✖       |          ✖          |        ✖         |       ✖       |          ✖          |             ✖              |         ✖         |
+---------+-----------------+---------------+---------------------+------------------+---------------+---------------------+----------------------------+-------------------+
|  1.1.0  |        ✖        |       ✖       |          ✖          |        ✖         |       ✖       |          ✖          |             ✖              |         ✖         |
+---------+-----------------+---------------+---------------------+------------------+---------------+---------------------+----------------------------+-------------------+
|  1.2.0  |        ✖        |       ✖       |          ✖          |        ✖         |       ✖       |          ✖          |             ✖              |         ✖         |
+---------+-----------------+---------------+---------------------+------------------+---------------+---------------------+----------------------------+-------------------+
|  1.2.1  |        ✔        |       ✖       |          ✖          |        ✖         |       ✖       |          ✖          |             ✖              |         ✖         |
+---------+-----------------+---------------+---------------------+------------------+---------------+---------------------+----------------------------+-------------------+
|  1.2.2  |        ✔        |       ✖       |          ✖          |        ✖         |       ✖       |          ✖          |             ✖              |         ✖         |
+---------+-----------------+---------------+---------------------+------------------+---------------+---------------------+----------------------------+-------------------+
|  1.3.0  |        ✔        |       ✖       |          ✖          |        ✖         |       ✖       |          ✖          |             ✖              |         ✖         |
+---------+-----------------+---------------+---------------------+------------------+---------------+---------------------+----------------------------+-------------------+
|  1.4.0  |        ✔        |       ✔       |          ✔          |        ✔         |       ✖       |          ✖          |             ✖              |         ✖         |
+---------+-----------------+---------------+---------------------+------------------+---------------+---------------------+----------------------------+-------------------+
|  1.4.1  |        ✔        |       ✔       |          ✔          |        ✔         |       ✖       |          ✖          |             ✖              |         ✖         |
+---------+-----------------+---------------+---------------------+------------------+---------------+---------------------+----------------------------+-------------------+
|  1.4.2  |        ✔        |       ✔       |          ✔          |        ✔         |       ✖       |          ✖          |             ✖              |         ✖         |
+---------+-----------------+---------------+---------------------+------------------+---------------+---------------------+----------------------------+-------------------+
|  1.4.3  |        ✔        |       ✔       |          ✔          |        ✔         |       ✖       |          ✖          |             ✖              |         ✖         |
+---------+-----------------+---------------+---------------------+------------------+---------------+---------------------+----------------------------+-------------------+
|  1.4.4  |        ✔        |       ✔       |          ✔          |        ✔         |       ✖       |          ✖          |             ✖              |         ✖         |
+---------+-----------------+---------------+---------------------+------------------+---------------+---------------------+----------------------------+-------------------+
|  1.5.0  |        ✔        |       ✔       |          ✔          |        ✔         |       ✔       |          ✔          |             ✖              |         ✖         |
+---------+-----------------+---------------+---------------------+------------------+---------------+---------------------+----------------------------+-------------------+
|  1.6.0  |        ✔        |       ✔       |          ✔          |        ✔         |       ✔       |          ✔          |             ✔              |         ✖         |
+---------+-----------------+---------------+---------------------+------------------+---------------+---------------------+----------------------------+-------------------+
|  1.7.0  |        ✔        |       ✔       |          ✔          |        ✔         |       ✔       |          ✔          |             ✔              |         ✖         |
+---------+-----------------+---------------+---------------------+------------------+---------------+---------------------+----------------------------+-------------------+
|  1.7.1  |        ✔        |       ✔       |          ✔          |        ✔         |       ✔       |          ✔          |             ✔              |         ✖         |
+---------+-----------------+---------------+---------------------+------------------+---------------+---------------------+----------------------------+-------------------+
|  1.8.0  |        ✔        |       ✔       |          ✔          |        ✔         |       ✔       |          ✔          |             ✔              |         ✔         |
+---------+-----------------+---------------+---------------------+------------------+---------------+---------------------+----------------------------+-------------------+
|  1.8.1  |        ✔        |       ✔       |          ✔          |        ✔         |       ✔       |          ✔          |             ✔              |         ✔         |
+---------+-----------------+---------------+---------------------+------------------+---------------+---------------------+----------------------------+-------------------+

.. _datetime: https://docs.python.org/3/library/datetime.html#datetime.datetime
.. _timezone: https://docs.python.org/3/library/datetime.html#timezone-objects
.. _AMMetadata: https://metamoth.readthedocs.io/en/latest/metamoth.html#metamoth.metadata.AMMetadata
