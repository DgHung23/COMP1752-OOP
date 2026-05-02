import tkinter as tk
import tkinter.scrolledtext as tkst
from tkinter import filedialog
import os
import random

try:
    import pygame
except ImportError:
    pygame = None

try:
    from PIL import Image, ImageTk
except ImportError:
    Image = None
    ImageTk = None

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
        self.library = library
        self.mixer_ready = False
        self.track_image = None

        self._build_UI()


    def _build_UI(self):

        self.window.geometry("1280x720")
        self.window.title("View Tracks")
        self.window.configure(bg="#121212")

        # for responsive resize
        for i in range(8):
            self.window.grid_columnconfigure(i, weight=1, uniform="track_view")
        self.window.grid_rowconfigure(3, weight=1)
        self.window.grid_rowconfigure(4, weight=1)
        self.window.grid_rowconfigure(5, weight=1)

        title_lbl = tk.Label(self.window,text="View Tracks",font="TkHeadingFont",bg="#121212",fg="#ff5500",)
        title_lbl.grid(row=0, column=0, columnspan=2, sticky="W", padx=(30, 10), pady=(22, 4))

        subtitle_lbl = tk.Label(self.window,text="Browse the library, inspect details, and play a selected track.",font="TkDefaultFont",bg="#121212",fg="#b8b8b8",)
        subtitle_lbl.grid(row=0, column=2, columnspan=6, sticky="E", padx=(10, 30), pady=(22, 4))

        list_tracks_btn = tk.Button(self.window,text="List All Tracks",command=self.list_tracks_clicked,font="TkDefaultFont",bg="#ff5500",fg="white",activebackground="#d94800",activeforeground="white",relief="flat",bd=0,width=16,)
        list_tracks_btn.grid(row=1, column=0, padx=(30, 10), pady=16, ipady=8, sticky="EW")

        enter_lbl = tk.Label(self.window,text="Enter Track Number",font="TkDefaultFont",bg="#121212",fg="#f5f5f5",)
        enter_lbl.grid(row=1, column=1, columnspan=2, padx=10, pady=16, sticky="E")

        self.input_txt = tk.Entry(self.window,width=8,font="TkDefaultFont",bg="#1e1e1e",fg="#f5f5f5",insertbackground="#ff5500",relief="flat",highlightbackground="#3a3a3a",highlightcolor="#ff5500",highlightthickness=2,)
        self.input_txt.grid(row=1, column=3, padx=10, pady=16, ipady=8, sticky="EW")

        check_track_btn = tk.Button(self.window,text="View Track",command=self.view_tracks_clicked,font="TkDefaultFont",bg="#2a2a2a",fg="#f5f5f5",activebackground="#3a3a3a",activeforeground="white",relief="flat",bd=0,width=14,)
        check_track_btn.grid(row=1, column=4, padx=10, pady=16, ipady=8, sticky="EW")

        library_lbl = tk.Label(self.window,text="Track Library",font="TkHeadingFont",bg="#121212",fg="#f5f5f5",)
        library_lbl.grid(row=2, column=0, columnspan=4, sticky="W", padx=(30, 10), pady=(8, 0))

        choose_image_btn = tk.Button(self.window,text="Choose Image",command=self.choose_image_clicked,font="TkDefaultFont",bg="#2a2a2a",fg="#f5f5f5",activebackground="#3a3a3a",activeforeground="white",relief="flat",bd=0,width=14,)
        choose_image_btn.grid(row=2, column=4, columnspan=2, sticky="EW", padx=(18, 8), pady=(8, 0))

        selected_lbl = tk.Label(self.window,text="Selected Track",font="TkHeadingFont",bg="#121212",fg="#f5f5f5",)
        selected_lbl.grid(row=2, column=6, columnspan=2, sticky="W", padx=(8, 30), pady=(8, 0))

        self.image_lbl = tk.Label(self.window,text="",bg="#1e1e1e",relief="flat",highlightbackground="#3a3a3a",highlightcolor="#ff5500",highlightthickness=2,)
        self.image_lbl.grid(row=3, column=4, columnspan=2, sticky="NSEW", padx=(18, 8), pady=(10, 12))

        self.list_txt = tkst.ScrolledText(self.window,width=72,height=24,wrap="none",font="TkFixedFont",bg="#1e1e1e",fg="#f5f5f5",insertbackground="#ff5500",relief="flat",highlightbackground="#3a3a3a",highlightcolor="#ff5500",highlightthickness=2,)
        self.list_txt.grid(row=3,rowspan=5,column=0,columnspan=4,sticky="NSEW",padx=(30, 15),pady=(10, 20),)

        self.track_txt = tk.Text(self.window,width=42,height=7,wrap="none",font="TkFixedFont",bg="#1e1e1e",fg="#f5f5f5",insertbackground="#ff5500",relief="flat",highlightbackground="#3a3a3a",highlightcolor="#ff5500",highlightthickness=2,)
        self.track_txt.grid(row=3, column=6, columnspan=2, sticky="NSEW", padx=(8, 30), pady=(10, 12))

        self.animation_canvas = tk.Canvas(self.window,width=420,height=165,bg="#181818",highlightbackground="#ff5500",highlightcolor="#ff5500",highlightthickness=2,bd=0,)
        self.animation_canvas.grid(row=4, column=4, columnspan=4, sticky="NSEW", padx=(18, 30), pady=(0, 12))

        play_btn = tk.Button(self.window,text="Play",width=12,command=self.play_track_clicked,font="TkDefaultFont",bg="#ff5500",fg="white",activebackground="#d94800",activeforeground="white",relief="flat",bd=0,)
        play_btn.grid(row=5, column=4, columnspan=2, padx=(18, 8), pady=(0, 10), ipady=10, sticky="EW")

        stop_btn = tk.Button(self.window,text="Stop",width=12,command=self.stop_track_clicked,font="TkDefaultFont",bg="#2a2a2a",fg="#f5f5f5",activebackground="#3a3a3a",activeforeground="white",relief="flat",bd=0,)
        stop_btn.grid(row=5, column=6, columnspan=2, padx=(8, 30), pady=(0, 10), ipady=10, sticky="EW")

        volume_lbl = tk.Label(self.window,text="Volume",font="TkDefaultFont",bg="#121212",fg="#f5f5f5",)
        volume_lbl.grid(row=6, column=4, padx=(18, 8), pady=(4, 0), sticky="E")

        self.volume_value = tk.IntVar(value=70)
        self.volume_scale = tk.Scale(self.window,from_=0,to=100,orient="horizontal",variable=self.volume_value,command=self.volume_changed,font="TkDefaultFont",bg="#121212",fg="#f5f5f5",activebackground="#ff5500",troughcolor="#333333",highlightthickness=0,bd=0,length=360,showvalue=True,)
        self.volume_scale.grid(row=6, column=5, columnspan=3, padx=(0, 30), pady=(4, 0), sticky="EW")

        self.status_lbl = tk.Label(self.window,text="",font="TkDefaultFont",bg="#121212",fg="#b8b8b8",)
        self.status_lbl.grid(row=8, column=0, columnspan=8, sticky="W", padx=30, pady=(0, 18))

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
            self.show_track_image(key)
        else:
            set_text(self.track_txt, f"Track {key} not found")
            self.clear_track_image()
            Popup(self.window, 0, f"Track {key} not found.")
        self.status_lbl.configure(text="View Track button was clicked!")

    def choose_image_clicked(self):
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

        image_path = filedialog.askopenfilename(parent=self.window,title="Choose track image",initialdir="./assets/imgs",filetypes=[("Image files", "*.png *.gif *.jpg *.jpeg *.bmp"), ("All files", "*.*")])
        if not image_path:
            Popup(self.window, 0, "Image selection was cancelled.")
            self.status_lbl.configure(text="Image selection was cancelled.")
            return

        self.library.set_image_path(key, image_path)
        self.view_tracks_clicked()
        self.status_lbl.configure(text=f'Image path for "{name}" was updated.')

    def clear_track_image(self):
        self.track_image = None
        self.image_lbl.configure(image="", text="")

    def resolve_image_path(self, raw_path):
        if os.path.isabs(raw_path):
            return os.path.normpath(raw_path)
        return os.path.normpath(os.path.join(os.path.dirname(__file__), raw_path))

    def show_track_image(self, key):
        raw_path = self.library.get_image_path(key)
        if not raw_path:
            self.clear_track_image()
            return

        image_path = self.resolve_image_path(raw_path)
        if not os.path.exists(image_path):
            self.clear_track_image()
            return

        try:
            self.window.update_idletasks()
            max_width = self.image_lbl.winfo_width() - 8
            max_height = self.image_lbl.winfo_height() - 8
            if max_width < 20:
                max_width = 240
            if max_height < 20:
                max_height = 130
            if Image is not None and ImageTk is not None:
                with Image.open(image_path) as image:
                    image.thumbnail((max_width, max_height))
                    self.track_image = ImageTk.PhotoImage(image.copy())
            else:
                image = tk.PhotoImage(file=image_path)
                scale = max((image.width() + max_width - 1) // max_width, (image.height() + max_height - 1) // max_height, 1)
                self.track_image = image.subsample(scale, scale)
            self.image_lbl.configure(image=self.track_image, text="")
        except (OSError, tk.TclError):
            self.clear_track_image()

    def list_tracks_clicked(self):
        track_list = self.library.list_all()
        set_text(self.list_txt, track_list)
        self.status_lbl.configure(text="List Tracks button was clicked!")

    def play_track_clicked(self):
        key = self.input_txt.get().strip()

        if not key: # number check
            Popup(self.window, 0, "Please enter a track number.")
            self.status_lbl.configure(text="No track number was entered.")
            return

        name = self.library.get_name(key)
        if name is None: # exist song check
            Popup(self.window, 0, f"Track {key} not found.")
            self.status_lbl.configure(text=f"Track {key} was not found.")
            return

        raw_path = self.library.get_path(key)
        if not raw_path: # path check
            Popup(self.window, 0, f'Track {key} does not have an audio file path.')
            self.status_lbl.configure(text=f'Track {key} does not have an audio file path.')
            return

        track_path = os.path.normpath(os.path.join(os.path.dirname(__file__), raw_path))
        if not os.path.exists(track_path): # file exists check
            Popup(self.window, 0, f'Audio file for track {key} was not found.')
            self.status_lbl.configure(text=f'Audio file for track {key} was not found.')
            return

        if pygame is None: # pygame import failsafe handle
            Popup(self.window, 0, "pygame is not installed, so audio playback is unavailable.")
            self.status_lbl.configure(text="pygame is not installed.")
            return

        try: # pygame mixer engine failsafe handle
            if not self.mixer_ready:
                pygame.mixer.init()
                self.mixer_ready = True

            pygame.mixer.music.load(track_path)
            pygame.mixer.music.set_volume(self.volume_scale.get() / 100)
            pygame.mixer.music.play()
            self.library.increment_play_count(key)
        except pygame.error as error:
            Popup(self.window, 0, f"Unable to play track {key}: {error}")
            self.status_lbl.configure(text=f"Unable to play track {key}.")
            return
        
        self.view_tracks_clicked()
        
        try: # animation failsafe handle
            self.start_visualizer()
        except Exception as error:
            self.status_lbl.configure(text="Audio visualizer failed to start.")
            return

        self.status_lbl.configure(text=f'Now playing "{name}".')

    def stop_track_clicked(self):
        if pygame is None or not self.mixer_ready:
            self.status_lbl.configure(text="No track is currently playing.")
            Popup(self.window, 0, "No track is currently playing.")
            return

        pygame.mixer.music.stop()

        try: # animation failsafe handle
            self.stop_visualizer()
        except Exception as error:
            self.status_lbl.configure(text="Audio visualizer failed to stop.")
            return

        self.status_lbl.configure(text="Playback stopped.")
        Popup(self.window, 1, "Playback stopped.")

    def volume_changed(self, value):
        volume = float(value) / 100
        if pygame is not None and self.mixer_ready:
            try:
                pygame.mixer.music.set_volume(volume)
            except pygame.error:
                return

        if hasattr(self, "status_lbl"):
            self.status_lbl.configure(text=f"Volume set to {int(float(value))}%.")

    def start_visualizer(self):
        self.bars = 40
        self.canvas_width = 660
        self.canvas_height = 165
        self.bar_width = self.canvas_width // self.bars
        self.visualizer_running = True
        self.animate_visualizer()

    def animate_visualizer(self):
        if not self.visualizer_running:
            return
    
        self.animation_canvas.delete("bars")
    
        center_y = self.canvas_height // 2
    
        for i in range(self.bars):
            height = random.randint(3, self.volume_value.get() + 3)
    
            x1 = i * self.bar_width
            x2 = x1 + self.bar_width - 2
    
            y1 = center_y - height
            y2 = center_y + height
    
            color = random.choice([
                "#ff5500",
                "#ff7733",
                "#ffaa66",
                "#ffd1b3"
            ])
    
            self.animation_canvas.create_rectangle(
                x1, y1, x2, y2,
                fill=color,
                outline="",
                tags="bars"
            )
    
        self.window.after(70, self.animate_visualizer)

    def stop_visualizer(self):
        self.visualizer_running = False
        self.animation_canvas.delete("bars")

if __name__ == "__main__":  # only runs when this file is run as a standalone
    window = tk.Tk()        # create a TK object
    fonts.configure()       # configure the fonts
    library = build_library()
    TrackViewer(window, library)     # open the TrackViewer GUI
    window.mainloop()       # run the window main loop, reacting to button presses, etc
