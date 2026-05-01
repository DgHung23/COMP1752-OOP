import tkinter as tk
import tkinter.scrolledtext as tkst
import os

try:
    import pygame
except ImportError:
    pygame = None

import font_manager as fonts
from song_repository import SongRepository
from track_library import TrackLibrary
from popup import Popup


FILE_PATH = "assets/song.csv"


def set_text(text_area, content):
    text_area.delete("1.0", tk.END)
    text_area.insert("1.0", content)


class TrackListCreator:
    def __init__(self, window, library):
        self.library = library
        self.playlist = []
        self.window = window
        self.mixer_ready = False
        self.current_playlist_index = 0
        self.current_track_duration = 0
        self.playback_after_id = None
        self._build_UI()

    def _build_UI(self):
        self.window.geometry("1280x720")
        self.window.title("Create Track List")
        self.window.configure(bg="#111111")

        for i in range(6):
            self.window.grid_columnconfigure(i, weight=1)
        self.window.grid_rowconfigure(3, weight=1)
        self.window.grid_rowconfigure(4, weight=1)

        title_lbl = tk.Label(self.window, text="Create Track List", font="TkHeadingFont", bg="#111111", fg="#ff5500")
        title_lbl.grid(row=0, column=0, columnspan=2, sticky="W", padx=24, pady=(22, 8))

        subtitle_lbl = tk.Label(self.window, text="Build your playlist from the track library.", font="TkDefaultFont", bg="#111111", fg="#b8b8b8")
        subtitle_lbl.grid(row=0, column=2, columnspan=4, sticky="E", padx=24, pady=(22, 8))

        list_tracks_btn = tk.Button(self.window, text="List All Tracks", command=self.list_tracks_clicked, font="TkDefaultFont", bg="#222222", fg="#f5f5f5", activebackground="#303030", activeforeground="white", relief="flat", bd=0)
        list_tracks_btn.grid(row=1, column=0, padx=(24, 8), pady=12, ipady=8, sticky="EW")

        enter_lbl = tk.Label(self.window, text="Track Number", font="TkDefaultFont", bg="#111111", fg="#f5f5f5")
        enter_lbl.grid(row=1, column=1, padx=8, pady=12, sticky="E")

        self.input_txt = tk.Entry(self.window, width=8, font="TkDefaultFont", bg="#181818", fg="#f5f5f5", insertbackground="#ff5500", relief="flat", highlightbackground="#343434", highlightcolor="#ff5500", highlightthickness=2)
        self.input_txt.grid(row=1, column=2, padx=8, pady=12, ipady=8, sticky="EW")

        add_track_btn = tk.Button(self.window, text="Add Track", command=self.add_track_clicked, font="TkDefaultFont", bg="#ff5500", fg="white", activebackground="#d94800", activeforeground="white", relief="flat", bd=0)
        add_track_btn.grid(row=1, column=3, padx=8, pady=12, ipady=8, sticky="EW")

        reset_playlist_btn = tk.Button(self.window, text="Reset Playlist", command=self.reset_playlist_clicked, font="TkDefaultFont", bg="#222222", fg="#f5f5f5", activebackground="#303030", activeforeground="white", relief="flat", bd=0)
        reset_playlist_btn.grid(row=1, column=4, columnspan=2, padx=(8, 24), pady=12, ipady=8, sticky="EW")

        library_lbl = tk.Label(self.window, text="All available tracks", font="TkHeadingFont", bg="#111111", fg="#f5f5f5")
        library_lbl.grid(row=2, column=0, columnspan=4, sticky="NW", padx=(24, 8), pady=(12, 0))

        playlist_lbl = tk.Label(self.window, text="Current Playlist", font="TkHeadingFont", bg="#111111", fg="#f5f5f5")
        playlist_lbl.grid(row=2, column=4, columnspan=2, sticky="NW", padx=(8, 24), pady=(12, 0))

        self.list_txt = tkst.ScrolledText(self.window, width=54, height=16, wrap="none", font="TkFixedFont", bg="#181818", fg="#f5f5f5", insertbackground="#ff5500", relief="flat", highlightbackground="#343434", highlightcolor="#ff5500", highlightthickness=2)
        self.list_txt.grid(row=3, rowspan=2, column=0, columnspan=3, sticky="NSEW", padx=(24, 8), pady=(8, 14))

        self.playlist_txt = tkst.ScrolledText(self.window, width=30, height=8, wrap="none", font="TkFixedFont", bg="#181818", fg="#f5f5f5", insertbackground="#ff5500", relief="flat", highlightbackground="#343434", highlightcolor="#ff5500", highlightthickness=2)
        self.playlist_txt.grid(row=3, column=3, columnspan=3, sticky="NSEW", padx=(8, 24), pady=(8, 8))

        play_list_btn = tk.Button(self.window, text="Play", command=self.play_playlist_clicked, font="TkDefaultFont", bg="#ff5500", fg="white", activebackground="#d94800", activeforeground="white", relief="flat", bd=0)
        play_list_btn.grid(row=4, column=3, padx=(8, 8), pady=(8, 14), ipady=8, sticky="NEW")

        self.now_playing_lbl = tk.Label(self.window, text="No track playing | Remaining: 0:00", font="TkDefaultFont", bg="#111111", fg="#f5f5f5", anchor="w", justify="left")
        self.now_playing_lbl.grid(row=4, column=4, columnspan=2, sticky="NEW", padx=(8, 24), pady=(14, 14))

        self.status_lbl = tk.Label(self.window, text="", font="TkDefaultFont", bg="#111111", fg="#b8b8b8")
        self.status_lbl.grid(row=5, column=0, columnspan=6, sticky="W", padx=24, pady=(0, 18))

        self.list_tracks_clicked()

    def add_track_clicked(self):
        key = self.input_txt.get().strip()
        if not key:
            self.status_lbl.configure(text="Please enter a track number.")
            Popup(self.window, 0, "Please enter a track number.")
            return

        name = self.library.get_name(key)
        if name is None:
            self.status_lbl.configure(text=f"Track {key} not found.")
            Popup(self.window, 0, f"Track {key} not found.")
            return

        self.playlist.append(key)
        self.refresh_playlist()
        self.status_lbl.configure(text=f'"{name}" was added to the playlist.')
        Popup(self.window, 1, f'"{name}" was added to the playlist.')
        self.input_txt.delete(0, tk.END)

    def play_playlist_clicked(self):
        if not self.playlist:
            self.status_lbl.configure(text="Add at least one track before playing the playlist.")
            Popup(self.window, 0, "Add at least one track before playing the playlist.")
            return

        if pygame is None:
            self.status_lbl.configure(text="pygame is not installed.")
            Popup(self.window, 0, "pygame is not installed, so audio playback is unavailable.")
            return

        self.stop_playlist_playback(False)
        self.current_playlist_index = 0
        self.play_current_playlist_track()

    def reset_playlist_clicked(self):
        if len(self.playlist) == 0:
            self.status_lbl.configure(text="The playlist is already empty.")
            Popup(self.window, 0, "The playlist is already empty.")
            return
        self.stop_playlist_playback(True)
        self.playlist = []
        set_text(self.playlist_txt, "")
        self.status_lbl.configure(text="The playlist was reset.")
        Popup(self.window, 1, "The playlist was reset.")

    def list_tracks_clicked(self):
        track_list = self.library.list_all()
        set_text(self.list_txt, track_list)

    def refresh_playlist(self):
        playlist_names = [self.library.get_name(key) for key in self.playlist]
        playlist_content = "\n".join(name for name in playlist_names if name is not None)
        set_text(self.playlist_txt, playlist_content)

    def play_current_playlist_track(self):
        if self.current_playlist_index >= len(self.playlist):
            self.finish_playlist_playback()
            return

        key = self.playlist[self.current_playlist_index]
        name = self.library.get_name(key)
        raw_path = self.library.get_path(key)
        if not raw_path:
            self.status_lbl.configure(text=f'Track {key} does not have an audio file path.')
            Popup(self.window, 0, f'Track {key} does not have an audio file path.')
            return

        track_path = os.path.normpath(os.path.join(os.path.dirname(__file__), raw_path))
        if not os.path.exists(track_path):
            self.status_lbl.configure(text=f'Audio file for track {key} was not found.')
            Popup(self.window, 0, f'Audio file for track {key} was not found.')
            return

        try:
            if not self.mixer_ready:
                pygame.mixer.init()
                self.mixer_ready = True

            pygame.mixer.music.load(track_path)
            pygame.mixer.music.set_volume(0.7)
            pygame.mixer.music.play()
            self.library.increment_play_count(key)
        except pygame.error as error:
            self.status_lbl.configure(text=f"Unable to play track {key}.")
            Popup(self.window, 0, f"Unable to play track {key}: {error}")
            return

        self.current_track_duration = max(0, self.library.get_duration(key))
        self.update_now_playing_label(name, self.current_track_duration)
        self.status_lbl.configure(text=f'Now playing "{name}".')
        self.schedule_playback_update()

    def schedule_playback_update(self):
        if self.playback_after_id is not None:
            self.window.after_cancel(self.playback_after_id)
        self.playback_after_id = self.window.after(1000, self.update_playlist_playback)

    def update_playlist_playback(self):
        if pygame is None or not self.mixer_ready:
            return

        self.playback_after_id = None
        key = self.playlist[self.current_playlist_index] if self.current_playlist_index < len(self.playlist) else None
        name = self.library.get_name(key) if key is not None else None
        elapsed_seconds = max(0, pygame.mixer.music.get_pos() // 1000)
        remaining_seconds = max(0, self.current_track_duration - elapsed_seconds)
        self.update_now_playing_label(name, remaining_seconds)

        if not pygame.mixer.music.get_busy() or remaining_seconds == 0:
            self.current_playlist_index += 1
            self.play_current_playlist_track()
            return

        self.schedule_playback_update()

    def update_now_playing_label(self, name, remaining_seconds):
        if name is None:
            self.now_playing_lbl.configure(text="No track playing | Remaining: 0:00")
            return

        self.now_playing_lbl.configure(text=f"Now playing: {name} | Remaining: {self.format_seconds(remaining_seconds)}")

    def finish_playlist_playback(self):
        self.playback_after_id = None
        self.update_now_playing_label(None, 0)
        self.status_lbl.configure(text="Playlist playback finished.")

    def stop_playlist_playback(self, reset_label=True):
        if self.playback_after_id is not None:
            self.window.after_cancel(self.playback_after_id)
            self.playback_after_id = None

        if pygame is not None and self.mixer_ready:
            pygame.mixer.music.stop()

        if reset_label:
            self.update_now_playing_label(None, 0)

    def format_seconds(self, seconds):
        minutes = seconds // 60
        seconds = seconds % 60
        return f"{minutes}:{seconds:02d}"


def build_library():
    repository = SongRepository(FILE_PATH)
    return TrackLibrary(repository)


if __name__ == "__main__": # block to run in standalone version
    window = tk.Tk() # create a Tkinter window
    fonts.configure() # configure fonts using the font_manager module
    library = build_library() # load the data from the song repository
    TrackListCreator(window, library) # create a view_track UI window with attached data library
    window.mainloop() # start Tkinter loop to keep the window open
