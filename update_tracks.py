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


class TrackUpdater:
    def __init__(self, window, library):
        self.library = library

        window.geometry("820x350")
        window.title("Update Tracks")

        list_tracks_btn = tk.Button(window, text="List All Tracks", command=self.list_tracks_clicked)
        list_tracks_btn.grid(row=0, column=0, padx=10, pady=10)

        enter_track_lbl = tk.Label(window, text="Enter Track Number")
        enter_track_lbl.grid(row=0, column=1, padx=10, pady=10)

        self.track_input_txt = tk.Entry(window, width=5)
        self.track_input_txt.grid(row=0, column=2, padx=10, pady=10)

        enter_rating_lbl = tk.Label(window, text="Enter New Rating")
        enter_rating_lbl.grid(row=0, column=3, padx=10, pady=10)

        self.rating_input_txt = tk.Entry(window, width=5)
        self.rating_input_txt.grid(row=0, column=4, padx=10, pady=10)

        update_track_btn = tk.Button(window, text="Update Track", command=self.update_track_clicked)
        update_track_btn.grid(row=0, column=5, padx=10, pady=10)

        self.list_txt = tkst.ScrolledText(window, width=48, height=12, wrap="none")
        self.list_txt.grid(row=1, column=0, columnspan=4, sticky="W", padx=10, pady=10)

        self.track_txt = tk.Text(window, width=26, height=6, wrap="none")
        self.track_txt.grid(row=1, column=4, columnspan=2, sticky="NW", padx=10, pady=10)

        self.status_lbl = tk.Label(window, text="", font=("Helvetica", 10))
        self.status_lbl.grid(row=2, column=0, columnspan=6, sticky="W", padx=10, pady=10)

        self.list_tracks_clicked()

    def update_track_clicked(self):
        key = self.track_input_txt.get().strip()
        rating_text = self.rating_input_txt.get().strip()

        if not key:
            set_text(self.track_txt, "Please enter a track number.")
            self.status_lbl.configure(text="No track number was entered.")
            Popup(window, 0, "Please enter a track number.")
            return

        name = self.library.get_name(key)
        if name is None:
            set_text(self.track_txt, f"Track {key} not found.")
            self.status_lbl.configure(text="The track number is invalid.")
            Popup(window, 0, f"Track {key} not found.")
            return

        try:
            rating = int(rating_text)
        except ValueError:
            set_text(self.track_txt, "Please enter a whole-number rating between 0 and 5.")
            self.status_lbl.configure(text="The rating is invalid.")
            Popup(window, 0, "the rating must be integer")
            return

        try:
            self.library.set_rating(key, rating)
        except ValueError as error:
            set_text(self.track_txt, str(error))
            self.status_lbl.configure(text="The rating is invalid.")
            Popup(window, 0, "the rating number must be between 0 and 5")
            return

        play_count = self.library.get_play_count(key)
        track_details = f"{name}\nnew rating: {rating}\nplays: {play_count}"
        set_text(self.track_txt, track_details)
        self.list_tracks_clicked()
        self.status_lbl.configure(text=f'Track {key} was updated.')
        Popup(window, 1, f'Track {key} was updated with a rating of {rating}.')

    def list_tracks_clicked(self):
        track_list = self.library.list_all()
        set_text(self.list_txt, track_list)


def build_library():
    repository = SongRepository(FILE_PATH)
    return TrackLibrary(repository)


if __name__ == "__main__":
    window = tk.Tk()
    fonts.configure()
    library = build_library()
    TrackUpdater(window, library)
    window.mainloop()
