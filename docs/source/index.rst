.. spotify-local-control documentation master file, created by
   sphinx-quickstart on Tue Feb 27 08:03:45 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Spotify-Local: A multi-platform API to control the local Spotify Client
===============================================================================

.. toctree::
   :maxdepth: 2
   :caption: Contents:

**Spotify-Local** library is designed to make controlling the Spotify client on your local machine possible!
This is a wrapper for the web helper process which exposes a simple api.
**Spotify-Local** is inspired by `SpotifyAPI-NET <https://github.com/JohnnyCrazy/SpotifyAPI-NET>`_.
This library allows you to perform simple actions quickly, or listen to events and register callbacks when
a song changes, or the pause button is pushed.

When using this library you automatically get:

- The ability to play/pause the current song
- The ability to change tracks
- You can register callbacks and listen for events when the state of Spotify changes
- A nice context manager api using `with`


Installation
============

.. code-block:: shell

    $ pipenv install spotify-local

Only **Python 3.3+** is supported.


Tutorial & Usage
================

Connect to the Spotify Client (Spotify must be open to do this):

.. code-block:: pycon

    >>> from spotify_local import SpotifyLocal

    >>> with SpotifyLocal() as s:
            pass

Pause the Spotify Client:

.. code-block:: pycon

    >>> with SpotifyLocal() as s:
            s.pause()


Grab the current state of the Spotify client, including now playing information:

.. code-block:: pycon

    >>> with SpotifyLocal() as s:
            print(s.get_current_status())

Play a playlist, song, album, artist, etc using a Spotify uri link:

.. code-block:: pycon

    >>> with SpotifyLocal() as s:
            s.playURI('spotify:track:0thLhIqWsqqycEqFONOyhu')

Register a callback and listen for events:

.. code-block:: pycon

    >>> from spotify_local import SpotifyLocal
    >>> s = SpotifyLocal()
    >>> @s.on('track_change')
    >>> def test(event):
    ...     print(event)
    >>> s.listen(blocking=False)
    >>> print("Do more stuff because that runs in the background")


License
=======
MIT


API Documentation
=================

Main Classes
------------

.. module:: spotify_local

These classes are the main interface to ``spotify_local``:


.. autoclass:: SpotifyLocal
    :inherited-members:


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`