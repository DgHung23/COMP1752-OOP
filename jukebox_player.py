import tkinter as tk
from PIL import Image, ImageTk, ImageOps

import font_manager as fonts
from create_track_list import TrackListCreator
from update_tracks import TrackUpdater
from view_tracks import TrackViewer
from song_repository import SongRepository 
from track_library import TrackLibrary


FILE_PATH = "assets/song.csv"
repository = SongRepository(FILE_PATH)
library = TrackLibrary(repository)

class JukeBoxApp:
    def __init__(self, window):
        self._window = window
        self._window.title("JukeBox")
        self._build_UI()

    def _build_UI(self):
        self._window.geometry("780x360")
        self._window.configure(bg="#121212")
        for i in range(3):
            self._window.grid_columnconfigure(i, weight=1, uniform="dashboard")
        library._library = library._repository.load()
        total_songs = len(library._library)
        total_artists = len({song._artist for song in library._library.values() if song._artist})
        logo_image = ImageOps.fit(Image.open("assets/imgs/logo.png"), (240, 160))
        self._logo_img = ImageTk.PhotoImage(logo_image)

        logo_lbl = tk.Label(self._window,image=self._logo_img,bg="#121212")
        logo_lbl.grid(row=0, column=0, padx=(28, 12), pady=(28, 18), sticky="NSEW")

        songs_lbl = tk.Label(self._window,text=f"{total_songs} songs loaded",font="TkHeadingFont",bg="#1e1e1e",fg="#ff5500",relief="flat",highlightbackground="#3a3a3a",highlightthickness=2)
        songs_lbl.grid(row=0, column=1, padx=12, pady=(28, 18), ipadx=10, ipady=42, sticky="NSEW")

        artists_lbl = tk.Label(self._window,text=f"{total_artists} total artist",font="TkHeadingFont",bg="#1e1e1e",fg="#f5f5f5",relief="flat",highlightbackground="#3a3a3a",highlightthickness=2)
        artists_lbl.grid(row=0, column=2, padx=(12, 28), pady=(28, 18), ipadx=10, ipady=42, sticky="NSEW")

        view_tracks_btn = tk.Button(self._window,text="View Tracks",command=self._view_tracks_clicked,font="TkDefaultFont",bg="#ff5500",fg="white",activebackground="#d94800",activeforeground="white",relief="flat",bd=0)
        view_tracks_btn.grid(row=1, column=0, padx=(28, 12), pady=(0, 18), ipady=12, sticky="EW")

        create_track_list_btn = tk.Button(self._window,text="Create Track List",command=self._create_track_list_clicked,font="TkDefaultFont",bg="#2a2a2a",fg="#f5f5f5",activebackground="#3a3a3a",activeforeground="white",relief="flat",bd=0)
        create_track_list_btn.grid(row=1, column=1, padx=12, pady=(0, 18), ipady=12, sticky="EW")

        update_tracks_btn = tk.Button(self._window,text="Update Tracks",command=self._update_tracks_clicked,font="TkDefaultFont",bg="#2a2a2a",fg="#f5f5f5",activebackground="#3a3a3a",activeforeground="white",relief="flat",bd=0)
        update_tracks_btn.grid(row=1, column=2, padx=(12, 28), pady=(0, 18), ipady=12, sticky="EW")

        self._status_lbl = tk.Label(self._window,text="",font="TkDefaultFont",bg="#121212",fg="#b8b8b8")
        self._status_lbl.grid(row=2, column=0, columnspan=3, padx=28, pady=(0, 24), sticky="W")

    def _view_tracks_clicked(self):
        self._status_lbl.configure(text="View Tracks button was clicked!")
        TrackViewer(tk.Toplevel(self._window), library)
    def _create_track_list_clicked(self):
        self._status_lbl.configure(text="Create Track List button was clicked!")
        TrackListCreator(tk.Toplevel(self._window), library)
    def _update_tracks_clicked(self):
        self._status_lbl.configure(text="Update Tracks button was clicked!")
        TrackUpdater(tk.Toplevel(self._window), library)

if __name__ == "__main__":
    window = tk.Tk()
    fonts.configure()
    app = JukeBoxApp(window)
    window.mainloop()
