========
metamoth
========

.. image:: https://img.shields.io/pypi/v/metamoth.svg
    :target: https://pypi.python.org/pypi/metamoth/
    :alt: PyPI

.. image:: https://github.com/mbsantiago/metamoth/workflows/Test/badge.svg?branch=main
    :target: https://github.com/mbsantiago/metamoth/actions?query=workflow%3ATest
    :alt: Test Status

.. image:: https://github.com/mbsantiago/metamoth/workflows/Lint/badge.svg?branch=main
    :target: https://github.com/mbsantiago/metamoth/actions?query=workflow%3ALint
    :alt: Lint Status

.. image:: https://codecov.io/gh/mbsantiago/metamoth/branch/main/graph/badge.svg
    :target: https://codecov.io/gh/mbsantiago/metamoth
    :alt: Code Coverage

.. image:: https://img.shields.io/github/license/mashape/apistatus.svg
    :target: https://pypi.python.org/pypi/metamoth/
    :alt: License

.. image:: https://pepy.tech/badge/metamoth
    :target: https://pepy.tech/project/metamoth
    :alt: Downloads

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/psf/black
    :alt: Code Style

.. image:: https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336
    :target: https://timothycrosley.github.io/isort/
    :alt: Imports

Metamoth is a Python package for parsing the metadata of AudioMoth_ files.
Check the full documentation at https://metamoth.readthedocs.io.

.. _AudioMoth: https://www.openacousticdevices.info/audiomoth

Motivation
==========

AudioMoth devices store valuable information in the audio file header. This
includes the device ID, the date and time of recording, gain
settings and battery state. The number of fields in the metadata is
growing as new features are added to the AudioMoth firmware.

However, the metadata is not designed to be easily parsed in a programmatic
way. The data is stored as a string comment making it difficult to retrieve the
individual metadata fields. Additionally, the comment format is not well
documented and changes between AudioMoth firmware versions.

This package helps by **quickly** parsing the metadata and returning an
object containing the metadata.

Usage
=====

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

Extracted Metadata
------------------

The ``metadata`` variable is an object (of type `AMMetadata`_) containing the
metadata of the file.

The extracted metadata contains:

* ``path``: the path of the audio file
* ``firmware_version``: the firmware version of the AudioMoth that
  recorded the file. Since the AudioMoth firmware version is not stored in the
  recording, this is an estimate and may be incorrect.

Media Information

* ``duration_s``: the duration of the file in seconds.
* ``samplerate_hz``: the sample rate of the file in Hz.
* ``channels``: the number of channels in the file.
* ``samples``: the number of audio samples in the file.

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

* ``recording_state``: the recording state of the AudioMoth that recorded
  the file.
* ``temperature_c``: the temperature of the AudioMoth in Celsius.
* ``amplitude_threshold``: information concerning the wether an amplitude
  threshold was used and the threshold value.
* ``frequency_filter``: information concerning the wether a frequency filter
  was used and the filter settings.
* ``deployment_id``: the deployment ID as set by the user.
* ``external_microphone``: a boolean indicating if an external microphone was
  used.
* ``minimum_trigger_duration_s``: the minimum trigger duration in seconds.
* ``frequency_trigger``: information concerning the wether a frequency trigger
  was used and the trigger settings.

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

Supported AudioMoth Firmware Versions
=====================================

In the table below you can find the supported AudioMoth firmware versions.

.. list-table:: Supported AudioMoth Firmware Versions
   :widths: 20 20
   :header-rows: 1

   * - Firmware
     - Supported
   * - 1.0.0
     - ✔
   * - 1.0.1
     - ✔
   * - 1.1.0
     - ✔
   * - 1.2.0
     - ✔
   * - 1.2.1
     - ✔
   * - 1.2.2
     - ✔
   * - 1.3.0
     - ✔
   * - 1.4.0
     - ✔
   * - 1.4.1
     - ✔
   * - 1.4.2
     - ✔
   * - 1.4.3
     - ✔
   * - 1.4.4
     - ✔
   * - 1.5.0
     - ✖
   * - 1.6.0
     - ✔
   * - 1.7.0
     - ✖
   * - 1.7.1
     - ✖
   * - 1.8.0
     - ✖
   * - 1.8.1
     - ✖


Support for newer firmware versions is planned, see the CONTRIBUTING_ section
if you want to help!

.. _CONTRIBUTING: https://github.com/mbsantiago/metamoth/blob/main/CONTRIBUTING.rst

Performance
===========

The ``metamoth`` package is designed to be fast. It extracts
all the required information from the first few bytes and avoids
loading the audio data. Thus ``metamoth`` parsing times are
not affected by the size of the audio file.

The following table shows the parsing times of ``metamoth`` compared to `exif tool`_.

+-----------------+-----------------+-----------------+-----------------+
| File Size (MB)  | metamoth (ms)   | exiftool (ms)   | Speedup         |
+=================+=================+=================+=================+
| 7.3             | 0.0845          | 80              | ~1000x          |
+-----------------+-----------------+-----------------+-----------------+
| 44              | 0.0850          | 91.86           | ~1000x          |
+-----------------+-----------------+-----------------+-----------------+


.. _exif tool: https://exiftool.org/

Installation
============

The ``metamoth`` package can be installed using ``pip``::

    pip install metamoth

Check the installation section of the documentation_ for more
information.

.. _documentation: https://metamoth.readthedocs.io/en/latest/installation.html

Documentation
=============

The documentation for the ``metamoth`` package is available at https://metamoth.readthedocs.io/en/latest/index.html.
