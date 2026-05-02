import tkinter as tk
import tkinter.scrolledtext as tkst

import font_manager as fonts
from song_repository import SongRepository
from track_library import TrackLibrary
from popup import Popup


FILE_PATH = "assets/song.csv"
# load data for standalone run
def _build_library():
    repository = SongRepository(FILE_PATH)
    return TrackLibrary(repository)


def _set_text(text_area, content):
    text_area.delete("1.0", tk.END)
    text_area.insert("1.0", content)


class TrackUpdater:
    def __init__(self, window, library):
        self._library = library
        self._window = window
        self._window.geometry("820x350")
        self._window.title("Update Tracks")

        self._build_UI()


    def _build_UI(self):
        self._window.geometry("960x520")
        self._window.configure(bg="#111111")

        self._window.grid_columnconfigure(0, weight=1)
        self._window.grid_columnconfigure(1, weight=1)
        self._window.grid_columnconfigure(2, weight=1)
        self._window.grid_columnconfigure(3, weight=1)
        self._window.grid_columnconfigure(4, weight=1)
        self._window.grid_columnconfigure(5, weight=1)
        self._window.grid_rowconfigure(3, weight=1)

        title_lbl = tk.Label(self._window, text="Update Tracks", font="TkHeadingFont", bg="#111111", fg="#ff5500")
        title_lbl.grid(row=0, column=0, columnspan=2, sticky="W", padx=24, pady=(22, 8))

        subtitle_lbl = tk.Label(self._window, text="Change ratings and review updated track details.", font="TkDefaultFont", bg="#111111", fg="#b8b8b8")
        subtitle_lbl.grid(row=0, column=2, columnspan=4, sticky="E", padx=24, pady=(22, 8))

        list_tracks_btn = tk.Button(self._window, text="List All Tracks", command=self._list_tracks_clicked, font="TkDefaultFont", bg="#222222", fg="#f5f5f5", activebackground="#303030", activeforeground="white", relief="flat", bd=0)
        list_tracks_btn.grid(row=1, column=0, padx=(24, 8), pady=12, ipady=8, sticky="EW")

        enter_track_lbl = tk.Label(self._window, text="Track Number", font="TkDefaultFont", bg="#111111", fg="#f5f5f5")
        enter_track_lbl.grid(row=1, column=1, padx=8, pady=12, sticky="E")

        self._track_input_txt = tk.Entry(self._window, width=8, font="TkDefaultFont", bg="#181818", fg="#f5f5f5", insertbackground="#ff5500", relief="flat", highlightbackground="#343434", highlightcolor="#ff5500", highlightthickness=2)
        self._track_input_txt.grid(row=1, column=2, padx=8, pady=12, ipady=8, sticky="EW")

        enter_rating_lbl = tk.Label(self._window, text="New Rating", font="TkDefaultFont", bg="#111111", fg="#f5f5f5")
        enter_rating_lbl.grid(row=1, column=3, padx=8, pady=12, sticky="E")

        self._rating_input_txt = tk.Entry(self._window, width=8, font="TkDefaultFont", bg="#181818", fg="#f5f5f5", insertbackground="#ff5500", relief="flat", highlightbackground="#343434", highlightcolor="#ff5500", highlightthickness=2)
        self._rating_input_txt.grid(row=1, column=4, padx=8, pady=12, ipady=8, sticky="EW")

        update_track_btn = tk.Button(self._window, text="Update Track", command=self._update_track_clicked, font="TkDefaultFont", bg="#ff5500", fg="white", activebackground="#d94800", activeforeground="white", relief="flat", bd=0)
        update_track_btn.grid(row=1, column=5, padx=(8, 24), pady=12, ipady=8, sticky="EW")

        library_lbl = tk.Label(self._window, text="Track Library", font="TkHeadingFont", bg="#111111", fg="#f5f5f5")
        library_lbl.grid(row=2, column=0, columnspan=4, sticky="NW", padx=(24, 8), pady=(12, 0))

        details_lbl = tk.Label(self._window, text="Updated Track", font="TkHeadingFont", bg="#111111", fg="#f5f5f5")
        details_lbl.grid(row=2, column=4, columnspan=2, sticky="NW", padx=(8, 24), pady=(12, 0))

        self._list_txt = tkst.ScrolledText(self._window, width=54, height=16, wrap="none", font="TkFixedFont", bg="#181818", fg="#f5f5f5", insertbackground="#ff5500", relief="flat", highlightbackground="#343434", highlightcolor="#ff5500", highlightthickness=2)
        self._list_txt.grid(row=3, column=0, columnspan=4, sticky="NSEW", padx=(24, 8), pady=(8, 14))

        self._track_txt = tk.Text(self._window, width=30, height=16, wrap="none", font="TkFixedFont", bg="#181818", fg="#f5f5f5", insertbackground="#ff5500", relief="flat", highlightbackground="#343434", highlightcolor="#ff5500", highlightthickness=2)
        self._track_txt.grid(row=3, column=4, columnspan=2, sticky="NSEW", padx=(8, 24), pady=(8, 14))

        self._status_lbl = tk.Label(self._window, text="", font="TkDefaultFont", bg="#111111", fg="#b8b8b8")
        self._status_lbl.grid(row=4, column=0, columnspan=6, sticky="W", padx=24, pady=(0, 18))

        self._list_tracks_clicked()

    def _update_track_clicked(self):
        key = self._track_input_txt.get().strip()
        rating_text = self._rating_input_txt.get().strip()

        if not key:
            _set_text(self._track_txt, "Please enter a track number.")
            self._status_lbl.configure(text="No track number was entered.")
            Popup(self._window, 0, "Please enter a track number.")
            return

        name = self._library.get_name(key)
        if name is None:
            _set_text(self._track_txt, f"Track {key} not found.")
            self._status_lbl.configure(text="The track number is invalid.")
            Popup(self._window, 0, f"Track {key} not found.")
            return

        try:
            rating = int(rating_text)
        except ValueError:
            _set_text(self._track_txt, "Please enter a integer rating between 0 and 5.")
            self._status_lbl.configure(text="The rating is invalid.")
            Popup(self._window, 0, "the rating must be integer")
            return

        try:
            self._library.set_rating(key, rating)
        except ValueError as error:
            _set_text(self._track_txt, str(error))
            self._status_lbl.configure(text="The rating is invalid.")
            Popup(self._window, 0, "the rating number must be between 0 and 5")
            return

        play_count = self._library.get_play_count(key)
        track_details = f"{name}\nnew rating: {rating}\nplays: {play_count}"
        _set_text(self._track_txt, track_details)
        self._list_tracks_clicked()
        self._status_lbl.configure(text=f'Track {key} was updated.')
        Popup(self._window, 1, f'Track {key} was updated with a rating of {rating}.')

    def _list_tracks_clicked(self):
        track_list = self._library.list_all()
        _set_text(self._list_txt, track_list)



if __name__ == "__main__":
    window = tk.Tk()
    fonts.configure()
    library = _build_library()
    TrackUpdater(window, library)
    window.mainloop()
