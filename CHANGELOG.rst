0.3.2 (2018-06-21)
==================

Features
--------

- You can now check if spotify and it's web helper are running and if not start
  them! (#2)
- Added decorators for track_change, status_change, and play_state_change, so
  the user doesn't have to type them out manually (#3)


0.3.0 (2018-06-20)
==================

Features
--------

- Added a new class that allows for async operations using asyncio (#0)
- Changed project name from "Spotify-Local-Control" to "Spotify-Local" (#1)
- `listen_for_events()` is now blocking, but uses new @on dectorator to call
  functions like in node.js (#2)
- You can now listen for three seperate events, `play_state_change`,
  `track_change`, and `status_change` (#3)
- `listen_for_events` can now be blocking or non-blocking (#4)
- refactored to use event emiiters! (#5)


0.2.3 (2018-06-15)
==================

Improved Documentation
----------------------

- Added doc strings to most functions (#0)
