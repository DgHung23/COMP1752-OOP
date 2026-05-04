# JukeBox Music Library

Coursework project for **COMP1752 Object-Oriented Programming**.

This project is a Python desktop application that manages and plays a small music library. It uses Tkinter for the graphical interface, CSV file storage for track data, and object-oriented classes to separate the song model, repository/data access, library logic, and GUI screens.

## Features

- View all tracks loaded from `assets/song.csv`
- Search for a track by track number
- Display track details including artist, rating, play count, and duration
- Play and stop individual MP3 tracks
- Adjust playback volume
- Show album/artist images for selected tracks
- Choose and save a new image for a track
- Create a temporary playlist and play tracks in sequence
- Update track ratings from 0 to 5
- Save updated ratings, play counts, and image paths back to the CSV file
- Basic popup feedback for success and error messages
- Pytest unit tests for the main track library logic

## Project Structure

```text
.
|-- jukebox_player.py       # Main application dashboard
|-- view_tracks.py          # View, inspect, and play individual tracks
|-- create_track_list.py    # Build and play a temporary playlist
|-- update_tracks.py        # Update track ratings
|-- track_library.py        # Core library operations
|-- song_repository.py      # CSV load/save logic
|-- song.py                 # Song model class
|-- popup.py                # Reusable popup window
|-- font_manager.py         # Shared font configuration
|-- unit_test.py            # Pytest test cases
|-- assets/
|   |-- song.csv            # Track data
|   |-- songs/              # MP3 audio files
|   |-- imgs/               # Track images and logo
```

## Object-Oriented Design

The application is organised around several classes:

- `Song` represents one track and stores its name, artist, rating, play count, duration, audio path, and image path.
- `SongRepository` handles loading and saving song data from the CSV file.
- `TrackLibrary` provides the main operations for getting track details, changing ratings, incrementing play counts, adding songs, and removing songs.
- `JukeBoxApp` builds the main menu window.
- `TrackViewer`, `TrackListCreator`, and `TrackUpdater` each manage a separate GUI workflow.
- `Popup` provides reusable success and error messages.

This separation keeps the data model, file storage, application logic, and user interface easier to understand and maintain.

## Requirements

- Python 3.10 or newer recommended
- Tkinter, usually included with standard Python installations
- Pillow, for image loading and resizing
- pygame, for MP3 playback
- pytest, for running tests

Install the external packages with:

```bash
pip install pillow pygame pytest
```

On Windows, if `pip` is not recognised, try:

```bash
py -m pip install pillow pygame pytest
```

## How to Run

From the project folder, run:

```bash
python jukebox_player.py
```

On Windows, you can also use:

```bash
py jukebox_player.py
```

The main dashboard opens with three options:

- **View Tracks**: browse tracks, view details, play music, change volume, and update track images.
- **Create Track List**: add tracks to a temporary playlist and play them in order.
- **Update Tracks**: change a track rating and save the result.

## Running Individual Windows

Each GUI module can also be run directly for testing:

```bash
python view_tracks.py
python create_track_list.py
python update_tracks.py
python popup.py
```

## Running Tests

Run the test suite with:

```bash
python -m pytest
```

Or on Windows:

```bash
py -m pytest
```

The tests in `unit_test.py` check important `TrackLibrary` behaviour, including valid and invalid track keys, rating updates, duplicate song handling, play count updates, and song removal.

## Data File

Track information is stored in:

```text
assets/song.csv
```

CSV columns:

- `id`: unique track number
- `name`: song name
- `artist`: artist name
- `rating`: rating from 0 to 5
- `play_count`: number of times the track has been played
- `duration`: track duration in seconds
- `path`: MP3 file path
- `image_path`: image file path

The application updates this file when ratings, play counts, or image paths change.

## Notes

- Keep the `assets` folder in the same directory as the Python files so the application can find the CSV, songs, and images.
- Audio playback requires `pygame`. If it is not installed, the application will still open, but playback will be unavailable.
- The bundled playlist is intended for coursework demonstration and testing.

## Coursework Information

- Module: **COMP1752 Object-Oriented Programming**
- Project: **JukeBox Music Library**
- Language: **Python**
- GUI Framework: **Tkinter**
- Data Storage: **CSV**
