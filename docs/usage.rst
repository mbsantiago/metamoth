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

The ``metadata`` variable is an object containing the metadata of the
file. It has the following attributes:

* ``path``: the title of the file
* ``duration``: the duration of the file in seconds
* ``samplerate``: the sample rate of the file in Hz
* ``channels``: the number of channels in the file
* ``samples``: the number of samples in the file
* ``datetime``: the date and time of the file in a datetime object
* ``gain``: the gain of the file
* ``timezone``: the timezone of the file.
* ``audiomoth_id``: the ID of the AudioMoth that recorded the file
* ``battery_state``: the battery state of the AudioMoth that recorded
  the file in Volts.

See the documentation of the :py:func:`metamoth.parse_metadata` function for more
information.

You can access any of these attributes as follows::

    duration = metadata.duration
    path = metadata.path
    # etc.

