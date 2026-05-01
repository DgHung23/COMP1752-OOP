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
        self.window = window
        self._build_UI()

    def _build_UI(self):
        self.window.geometry("960x520")
        self.window.title("Create Track List")
        self.window.configure(bg="#111111")

        for i in range(6):
            self.window.grid_columnconfigure(i, weight=1)
        self.window.grid_rowconfigure(3, weight=1)

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

        play_list_btn = tk.Button(self.window, text="Play Playlist", command=self.play_playlist_clicked, font="TkDefaultFont", bg="#222222", fg="#f5f5f5", activebackground="#303030", activeforeground="white", relief="flat", bd=0)
        play_list_btn.grid(row=1, column=4, padx=8, pady=12, ipady=8, sticky="EW")

        reset_playlist_btn = tk.Button(self.window, text="Reset Playlist", command=self.reset_playlist_clicked, font="TkDefaultFont", bg="#222222", fg="#f5f5f5", activebackground="#303030", activeforeground="white", relief="flat", bd=0)
        reset_playlist_btn.grid(row=1, column=5, padx=(8, 24), pady=12, ipady=8, sticky="EW")

        library_lbl = tk.Label(self.window, text="Track Library", font="TkHeadingFont", bg="#111111", fg="#f5f5f5")
        library_lbl.grid(row=2, column=0, columnspan=4, sticky="NW", padx=(24, 8), pady=(12, 0))

        playlist_lbl = tk.Label(self.window, text="Playlist", font="TkHeadingFont", bg="#111111", fg="#f5f5f5")
        playlist_lbl.grid(row=2, column=4, columnspan=2, sticky="NW", padx=(8, 24), pady=(12, 0))

        self.list_txt = tkst.ScrolledText(self.window, width=54, height=16, wrap="none", font="TkFixedFont", bg="#181818", fg="#f5f5f5", insertbackground="#ff5500", relief="flat", highlightbackground="#343434", highlightcolor="#ff5500", highlightthickness=2)
        self.list_txt.grid(row=3, column=0, columnspan=4, sticky="NSEW", padx=(24, 8), pady=(8, 14))

        self.playlist_txt = tk.Text(self.window, width=30, height=16, wrap="none", font="TkFixedFont", bg="#181818", fg="#f5f5f5", insertbackground="#ff5500", relief="flat", highlightbackground="#343434", highlightcolor="#ff5500", highlightthickness=2)
        self.playlist_txt.grid(row=3, column=4, columnspan=2, sticky="NSEW", padx=(8, 24), pady=(8, 14))

        self.status_lbl = tk.Label(self.window, text="", font="TkDefaultFont", bg="#111111", fg="#b8b8b8")
        self.status_lbl.grid(row=4, column=0, columnspan=6, sticky="W", padx=24, pady=(0, 18))

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

        for key in self.playlist:
            self.library.increment_play_count(key)

        self.status_lbl.configure(
            text=f"Simulated playlist playback for {len(self.playlist)} track(s)."
        )

    def reset_playlist_clicked(self):
        if len(self.playlist) == 0:
            self.status_lbl.configure(text="The playlist is already empty.")
            Popup(self.window, 0, "The playlist is already empty.")
            return
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


def build_library():
    repository = SongRepository(FILE_PATH)
    return TrackLibrary(repository)


if __name__ == "__main__": # block to run in standalone version
    window = tk.Tk() # create a Tkinter window
    fonts.configure() # configure fonts using the font_manager module
    library = build_library() # load the data from the song repository
    TrackListCreator(window, library) # create a view_track UI window with attached data library
    window.mainloop() # start Tkinter loop to keep the window open
