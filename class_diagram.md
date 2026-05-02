# Jukebox Project Class Diagram

```mermaid
classDiagram
    class Song {
        #_name: str
        #_artist: str
        #_rating: int
        #_play_count: int
        #_duration: int
        #_path: str
        #_image_path: str
        +__init__(name: str, artist: str, rating: int, play_count: int, duration: int, path: str, image_path: str): None
        +info(): str
        +stars(): str
        +set_rating(rating: int): None
        +increment_play_count(): None
        +formatted_duration(): str
        +to_dict(): Dict~str, Any~
        +from_dict(data: Dict~str, Any~): Song
    }

    class SongRepository {
        #_file_path: str
        +__init__(file_path: str): None
        +load(): Dict~str, Song~
        +save(songs: Dict~str, Song~): None
    }

    class TrackLibrary {
        #_repository: SongRepository
        #_library: Dict~str, Song~
        +__init__(repository: SongRepository): None
        +list_all(): str
        #_normalize_key(key: Any): Optional~str~
        #_get_song(key: Any): Optional~Song~
        +get_name(key: Any): Optional~str~
        +get_artist(key: Any): Optional~str~
        +get_rating(key: Any): int
        +get_play_count(key: Any): int
        +get_duration(key: Any): int
        +get_formatted_duration(key: Any): Optional~str~
        +get_path(key: Any): Optional~str~
        +get_image_path(key: Any): Optional~str~
        +set_rating(key: Any, rating: int): None
        +set_image_path(key: Any, image_path: str): None
        +increment_play_count(key: Any): None
        +add_song(key: Any, name: str, artist: str, rating: int, play_count: int, duration: int, path: str, image_path: str): None
        +remove_song(key: Any): None
    }

    class JukeBoxApp {
        #_window: tk.Misc
        #_logo_img: ImageTk.PhotoImage
        #_status_lbl: tk.Label
        +__init__(window: tk.Misc): None
        #_build_UI(): None
        #_view_tracks_clicked(): None
        #_create_track_list_clicked(): None
        #_update_tracks_clicked(): None
    }

    class TrackViewer {
        #_window: tk.Misc
        #_library: TrackLibrary
        #_mixer_ready: bool
        #_track_image: Optional~PhotoImage~
        #_input_txt: tk.Entry
        #_image_lbl: tk.Label
        #_list_txt: tkst.ScrolledText
        #_track_txt: tk.Text
        #_animation_canvas: tk.Canvas
        #_volume_value: tk.IntVar
        #_volume_scale: tk.Scale
        #_status_lbl: tk.Label
        #_bars: int
        #_canvas_width: int
        #_canvas_height: int
        #_bar_width: int
        #_visualizer_running: bool
        +__init__(window: tk.Misc, library: TrackLibrary): None
        #_build_UI(): None
        #_view_tracks_clicked(): None
        #_choose_image_clicked(): None
        #_clear_track_image(): None
        #_resolve_image_path(raw_path: str): str
        #_show_track_image(key: Any): None
        #_list_tracks_clicked(): None
        #_play_track_clicked(): None
        #_stop_track_clicked(): None
        #_volume_changed(value: str): None
        #_start_visualizer(): None
        #_animate_visualizer(): None
        #_stop_visualizer(): None
    }

    class TrackListCreator {
        #_library: TrackLibrary
        #_playlist: List~str~
        #_window: tk.Misc
        #_mixer_ready: bool
        #_current_playlist_index: int
        #_current_track_duration: int
        #_playback_after_id: Optional~str~
        #_input_txt: tk.Entry
        #_list_txt: tkst.ScrolledText
        #_playlist_txt: tkst.ScrolledText
        #_now_playing_lbl: tk.Label
        #_status_lbl: tk.Label
        +__init__(window: tk.Misc, library: TrackLibrary): None
        #_build_UI(): None
        #_add_track_clicked(): None
        #_play_playlist_clicked(): None
        #_reset_playlist_clicked(): None
        #_list_tracks_clicked(): None
        #_refresh_playlist(): None
        #_play_current_playlist_track(): None
        #_schedule_playback_update(): None
        #_update_playlist_playback(): None
        #_update_now_playing_label(name: Optional~str~, remaining_seconds: int): None
        #_finish_playlist_playback(): None
        #_stop_playlist_playback(reset_label: bool): None
        #_format_seconds(seconds: int): str
    }

    class TrackUpdater {
        #_library: TrackLibrary
        #_window: tk.Misc
        #_track_input_txt: tk.Entry
        #_rating_input_txt: tk.Entry
        #_list_txt: tkst.ScrolledText
        #_track_txt: tk.Text
        #_status_lbl: tk.Label
        +__init__(window: tk.Misc, library: TrackLibrary): None
        #_build_UI(): None
        #_update_track_clicked(): None
        #_list_tracks_clicked(): None
    }

    class Popup {
        #_parent: tk.Misc
        #_popup_type: int
        #_message: str
        #_window: tk.Toplevel
        +__init__(parent: tk.Misc, popup_type: int, message: str): None
        #_build_UI(): None
        #_center_window(): None
        #_close_popup(): None
    }

    SongRepository ..> Song : creates and saves
    TrackLibrary o-- SongRepository : has repository
    TrackLibrary o-- "0..*" Song : stores songs
    JukeBoxApp ..> TrackLibrary : uses shared library
    JukeBoxApp ..> TrackViewer : opens
    JukeBoxApp ..> TrackListCreator : opens
    JukeBoxApp ..> TrackUpdater : opens
    TrackViewer --> TrackLibrary : reads and updates
    TrackListCreator --> TrackLibrary : reads and updates
    TrackUpdater --> TrackLibrary : reads and updates
    TrackViewer ..> Popup : shows
    TrackListCreator ..> Popup : shows
    TrackUpdater ..> Popup : shows
```

## Relationship Summary

- `Song` is the data object for one track. Its state is protected, and public methods expose behavior such as rating updates, play count updates, duration formatting, and CSV conversion.
- `SongRepository` loads and saves `Song` objects from `assets/song.csv`. Its file path is protected because only the repository should use it directly.
- `TrackLibrary` is the main public service API. UI classes call its public getter/update methods instead of accessing songs directly.
- `JukeBoxApp` is the dashboard window. Its UI widgets and button callbacks are protected implementation details.
- `TrackViewer`, `TrackListCreator`, and `TrackUpdater` are Tkinter UI classes that receive and use the same `TrackLibrary` object. Their widget state, callbacks, and playback helpers are protected.
- `Popup` is a reusable notification window. Its window state and close callback are protected implementation details.

## Notes

- `+` means public and `#` means protected.
- No double-underscore private members are used because Python projects usually reserve `__private` for name-mangling cases.
- Types are inferred from constructor values, return values, and Tkinter/Pygame usage because the Python source does not declare type hints.
- Module-level helpers such as `_build_library()` and `_set_text()` are not modeled as classes.
