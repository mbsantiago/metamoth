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
AudioMoth devices store the device ID, the date and time of recording, gain
settings and battery state in a comment in the metadata header of the audio
file. This package helps by **quickly** parsing the metadata and returning an
object containing the metadata.

.. _AudioMoth: https://www.openacousticdevices.info/audiomoth


Usage
=====

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
* ``timezone``: the timezone of the file. See the timezone information
  below.
* ``audiomoth_id``: the ID of the AudioMoth that recorded the file
* ``battery_state``: the battery state of the AudioMoth that recorded
  the file in Volts.

You can access any of these attributes as follows::

.. code-block:: python

    duration = metadata.duration
    path = metadata.path
    # etc.

Installation
============

The ``metamoth`` package can be installed using ``pip``::

    pip install metamoth

If you prefer to use conda, you can install the package from the
conda-forge channel::

    conda install -c conda-forge metamoth

Check the installation section of the documentation_ for more
information.

.. _documentation: https://mbsantiago.github.io/metamoth/installation.html

Documentation
=============

The documentation for the ``metamoth`` package is available at https://mbsantiago.github.io/metamoth/.
