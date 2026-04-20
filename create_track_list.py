import tkinter as tk
import tkinter.scrolledtext as tkst

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

        window.geometry("860x360")
        window.title("Create Track List")

        list_tracks_btn = tk.Button(window, text="List All Tracks", command=self.list_tracks_clicked)
        list_tracks_btn.grid(row=0, column=0, padx=10, pady=10)

        enter_lbl = tk.Label(window, text="Enter Track Number")
        enter_lbl.grid(row=0, column=1, padx=10, pady=10)

        self.input_txt = tk.Entry(window, width=5)
        self.input_txt.grid(row=0, column=2, padx=10, pady=10)

        add_track_btn = tk.Button(window, text="Add Track", command=self.add_track_clicked)
        add_track_btn.grid(row=0, column=3, padx=10, pady=10)

        play_list_btn = tk.Button(window, text="Play Playlist", command=self.play_playlist_clicked)
        play_list_btn.grid(row=0, column=4, padx=10, pady=10)

        reset_playlist_btn = tk.Button(window, text="Reset Playlist", command=self.reset_playlist_clicked)
        reset_playlist_btn.grid(row=0, column=5, padx=10, pady=10)

        self.list_txt = tkst.ScrolledText(window, width=48, height=12, wrap="none")
        self.list_txt.grid(row=1, column=0, columnspan=4, sticky="W", padx=10, pady=10)

        playlist_lbl = tk.Label(window, text="Playlist")
        playlist_lbl.grid(row=1, column=4, columnspan=2, sticky="W", padx=10, pady=(10, 0))

        self.playlist_txt = tk.Text(window, width=28, height=12, wrap="none")
        self.playlist_txt.grid(row=1, column=4, columnspan=2, sticky="NW", padx=10, pady=(35, 10))

        self.status_lbl = tk.Label(window, text="", font=("Helvetica", 10))
        self.status_lbl.grid(row=2, column=0, columnspan=6, sticky="W", padx=10, pady=10)

        self.list_tracks_clicked()

    def add_track_clicked(self):
        key = self.input_txt.get().strip()
        if not key:
            self.status_lbl.configure(text="Please enter a track number.")
            Popup(window, 0, "Please enter a track number.")
            return

        name = self.library.get_name(key)
        if name is None:
            self.status_lbl.configure(text=f"Track {key} not found.")
            Popup(window, 0, f"Track {key} not found.")
            return

        self.playlist.append(key)
        self.refresh_playlist()
        self.status_lbl.configure(text=f'"{name}" was added to the playlist.')
        Popup(window, 1, f'"{name}" was added to the playlist.')
        self.input_txt.delete(0, tk.END)

    def play_playlist_clicked(self):
        if not self.playlist:
            self.status_lbl.configure(text="Add at least one track before playing the playlist.")
            Popup(window, 0, "Add at least one track before playing the playlist.")
            return

        for key in self.playlist:
            self.library.increment_play_count(key)

        self.status_lbl.configure(
            text=f"Simulated playlist playback for {len(self.playlist)} track(s)."
        )

    def reset_playlist_clicked(self):
        if len(self.playlist) == 0:
            self.status_lbl.configure(text="The playlist is already empty.")
            Popup(window, 0, "The playlist is already empty.")
            return
        self.playlist = []
        set_text(self.playlist_txt, "")
        self.status_lbl.configure(text="The playlist was reset.")
        Popup(window, 1, "The playlist was reset.")

    def list_tracks_clicked(self):
        track_list = self.library.list_all()
        set_text(self.list_txt, track_list)

    def refresh_playlist(self):
        playlist_names = [self.library.get_name(key) for key in self.playlist]
        playlist_content = "\n".join(name for name in playlist_names if name is not None)
        set_text(self.playlist_txt, playlist_content)


def build_library():
    repository = SongRepository(FILE_PATH)
    return TrackLibrary(repository)


if __name__ == "__main__":
    window = tk.Tk()
    fonts.configure()
    library = build_library()
    TrackListCreator(window, library)
    window.mainloop()
