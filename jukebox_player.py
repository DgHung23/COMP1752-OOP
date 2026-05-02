import tkinter as tk


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
        self.window = window
        self.window.geometry("520x150")
        self.window.title("JukeBox")
        self.window.configure(bg="gray")
        self.build_UI()

    def build_UI(self):
        header_lbl = tk.Label(self.window, text="Select an option by clicking one of the buttons below")
        header_lbl.grid(row=0, column=0, columnspan=3, padx=10, pady=10)

        view_tracks_btn = tk.Button(self.window, text="View Tracks", command=self.view_tracks_clicked)
        view_tracks_btn.grid(row=1, column=0, padx=10, pady=10)

        create_track_list_btn = tk.Button(self.window, text="Create Track List", command=self.create_track_list_clicked)
        create_track_list_btn.grid(row=1, column=1, padx=10, pady=10)

        update_tracks_btn = tk.Button(self.window, text="Update Tracks", command=self.update_tracks_clicked)
        update_tracks_btn.grid(row=1, column=2, padx=10, pady=10)

        self.status_lbl = tk.Label(self.window, bg='gray', text="", font=("Helvetica", 10))
        self.status_lbl.grid(row=2, column=0, columnspan=3, padx=10, pady=10)

    def view_tracks_clicked(self):
        self.status_lbl.configure(text="View Tracks button was clicked!")
        TrackViewer(tk.Toplevel(self.window), library)
    def create_track_list_clicked(self):
        self.status_lbl.configure(text="Create Track List button was clicked!")
        TrackListCreator(tk.Toplevel(self.window), library)
    def update_tracks_clicked(self):
        self.status_lbl.configure(text="Update Tracks button was clicked!")
        TrackUpdater(tk.Toplevel(self.window), library)

if __name__ == "__main__":
    window = tk.Tk()
    fonts.configure()
    app = JukeBoxApp(window)
    window.mainloop()