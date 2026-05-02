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
        from PIL import Image, ImageTk, ImageOps

        self.window.geometry("780x360")
        self.window.configure(bg="#121212")
        for i in range(3):
            self.window.grid_columnconfigure(i, weight=1, uniform="dashboard")
        library.library = library.repository.load()
        total_songs = len(library.library)
        total_artists = len({song.artist for song in library.library.values() if song.artist})
        logo_image = ImageOps.fit(Image.open("assets/imgs/logo.png"), (240, 160))
        self.logo_img = ImageTk.PhotoImage(logo_image)

        logo_lbl = tk.Label(self.window,image=self.logo_img,bg="#121212")
        logo_lbl.grid(row=0, column=0, padx=(28, 12), pady=(28, 18), sticky="NSEW")

        songs_lbl = tk.Label(self.window,text=f"{total_songs} songs loaded",font="TkHeadingFont",bg="#1e1e1e",fg="#ff5500",relief="flat",highlightbackground="#3a3a3a",highlightthickness=2)
        songs_lbl.grid(row=0, column=1, padx=12, pady=(28, 18), ipadx=10, ipady=42, sticky="NSEW")

        artists_lbl = tk.Label(self.window,text=f"{total_artists} total artist",font="TkHeadingFont",bg="#1e1e1e",fg="#f5f5f5",relief="flat",highlightbackground="#3a3a3a",highlightthickness=2)
        artists_lbl.grid(row=0, column=2, padx=(12, 28), pady=(28, 18), ipadx=10, ipady=42, sticky="NSEW")

        view_tracks_btn = tk.Button(self.window,text="View Tracks",command=self.view_tracks_clicked,font="TkDefaultFont",bg="#ff5500",fg="white",activebackground="#d94800",activeforeground="white",relief="flat",bd=0)
        view_tracks_btn.grid(row=1, column=0, padx=(28, 12), pady=(0, 18), ipady=12, sticky="EW")

        create_track_list_btn = tk.Button(self.window,text="Create Track List",command=self.create_track_list_clicked,font="TkDefaultFont",bg="#2a2a2a",fg="#f5f5f5",activebackground="#3a3a3a",activeforeground="white",relief="flat",bd=0)
        create_track_list_btn.grid(row=1, column=1, padx=12, pady=(0, 18), ipady=12, sticky="EW")

        update_tracks_btn = tk.Button(self.window,text="Update Tracks",command=self.update_tracks_clicked,font="TkDefaultFont",bg="#2a2a2a",fg="#f5f5f5",activebackground="#3a3a3a",activeforeground="white",relief="flat",bd=0)
        update_tracks_btn.grid(row=1, column=2, padx=(12, 28), pady=(0, 18), ipady=12, sticky="EW")

        self.status_lbl = tk.Label(self.window,text="",font="TkDefaultFont",bg="#121212",fg="#b8b8b8")
        self.status_lbl.grid(row=2, column=0, columnspan=3, padx=28, pady=(0, 24), sticky="W")

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
