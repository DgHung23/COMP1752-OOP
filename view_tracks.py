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
# load data for standalone run
def build_library(): 
    repository = SongRepository(FILE_PATH)
    return TrackLibrary(repository)


def set_text(text_area, content):
    text_area.delete("1.0", tk.END)
    text_area.insert(1.0, content)


class TrackViewer():
    def __init__(self, window, library):
        self.window = window
        window.geometry("750x350")
        window.title("View Tracks")
        self.library = library
        self.mixer_ready = False

        list_tracks_btn = tk.Button(window, text="List All Tracks", command=self.list_tracks_clicked)
        list_tracks_btn.grid(row=0, column=0, padx=10, pady=10)

        enter_lbl = tk.Label(window, text="Enter Track Number")
        enter_lbl.grid(row=0, column=1, padx=10, pady=10)

        self.input_txt = tk.Entry(window, width=5)
        self.input_txt.grid(row=0, column=2, padx=10, pady=10)

        check_track_btn = tk.Button(window, text="View Track", command=self.view_tracks_clicked)
        check_track_btn.grid(row=0, column=3, padx=10, pady=10)

        self.list_txt = tkst.ScrolledText(window, width=48, height=12, wrap="none", font="TkFixedFont")
        self.list_txt.grid(row=1, rowspan=2, column=0, columnspan=3, sticky="W", padx=10, pady=10)

        self.track_txt = tk.Text(window, width=24, height=5, wrap="none", font="TkFixedFont")
        self.track_txt.grid(row=1, column=3, columnspan=2, sticky="NW", padx=10, pady=10)

        # controls_frame = tk.Frame(window)
        # controls_frame.grid(row=2, column=3, sticky="W", padx=10, pady=(0, 10))

        play_btn = tk.Button(window, text="Play", width=10, command=self.play_track_clicked)
        play_btn.grid(row=2, column=3, padx=(0, 10))

        stop_btn = tk.Button(window, text="Stop", width=10, command=self.stop_track_clicked)
        stop_btn.grid(row=2, column=4)

        self.status_lbl = tk.Label(window, text="", font=("Helvetica", 10))
        self.status_lbl.grid(row=3, column=0, columnspan=4, sticky="W", padx=10, pady=10)

        self.list_tracks_clicked()

    def view_tracks_clicked(self):
        key = self.input_txt.get().strip()
        name = self.library.get_name(key)
        if name is not None:
            artist = self.library.get_artist(key)
            rating = self.library.get_rating(key)
            play_count = self.library.get_play_count(key)
            duration = self.library.get_formatted_duration(key)
            track_details = f"{name}\n{artist}\nrating: {rating}\nplays: {play_count}\nduration: {duration}"
            set_text(self.track_txt, track_details)
        else:
            set_text(self.track_txt, f"Track {key} not found")
            Popup(self.window, 0, f"Track {key} not found.")
        self.status_lbl.configure(text="View Track button was clicked!")

    def list_tracks_clicked(self):
        track_list = self.library.list_all()
        set_text(self.list_txt, track_list)
        self.status_lbl.configure(text="List Tracks button was clicked!")

    def play_track_clicked(self):
        key = self.input_txt.get().strip()

        if not key:
            Popup(self.window, 0, "Please enter a track number.")
            self.status_lbl.configure(text="No track number was entered.")
            return

        name = self.library.get_name(key)
        if name is None:
            Popup(self.window, 0, f"Track {key} not found.")
            self.status_lbl.configure(text=f"Track {key} was not found.")
            return

        raw_path = self.library.get_path(key)
        if not raw_path:
            Popup(self.window, 0, f'Track {key} does not have an audio file path.')
            self.status_lbl.configure(text=f'Track {key} does not have an audio file path.')
            return

        track_path = os.path.normpath(os.path.join(os.path.dirname(__file__), raw_path))
        if not os.path.exists(track_path):
            Popup(self.window, 0, f'Audio file for track {key} was not found.')
            self.status_lbl.configure(text=f'Audio file for track {key} was not found.')
            return

        if pygame is None:
            Popup(self.window, 0, "pygame is not installed, so audio playback is unavailable.")
            self.status_lbl.configure(text="pygame is not installed.")
            return

        try:
            if not self.mixer_ready:
                pygame.mixer.init()
                self.mixer_ready = True

            pygame.mixer.music.load(track_path)
            pygame.mixer.music.play()
        except pygame.error as error:
            Popup(self.window, 0, f"Unable to play track {key}: {error}")
            self.status_lbl.configure(text=f"Unable to play track {key}.")
            return

        self.view_tracks_clicked()
        self.status_lbl.configure(text=f'Now playing "{name}".')

    def stop_track_clicked(self):
        if pygame is None or not self.mixer_ready:
            self.status_lbl.configure(text="No track is currently playing.")
            Popup(self.window, 0, "No track is currently playing.")
            return

        pygame.mixer.music.stop()
        self.status_lbl.configure(text="Playback stopped.")
        Popup(self.window, 1, "Playback stopped.")

if __name__ == "__main__":  # only runs when this file is run as a standalone
    window = tk.Tk()        # create a TK object
    fonts.configure()       # configure the fonts
    library = build_library()
    TrackViewer(window, library)     # open the TrackViewer GUI
    window.mainloop()       # run the window main loop, reacting to button presses, etc
