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
def _build_library(): 
    repository = SongRepository(FILE_PATH)
    return TrackLibrary(repository)


def _set_text(text_area, content):
    text_area.delete("1.0", tk.END)
    text_area.insert(1.0, content)


class TrackViewer():
    def __init__(self, window, library):
        self._window = window
        self._library = library
        self._mixer_ready = False
        self._track_image = None

        self._build_UI()


    def _build_UI(self):

        self._window.geometry("1280x720")
        self._window.title("View Tracks")
        self._window.configure(bg="#121212")

        # for responsive resize
        for i in range(8):
            self._window.grid_columnconfigure(i, weight=1, uniform="track_view")
        self._window.grid_rowconfigure(3, weight=1)
        self._window.grid_rowconfigure(4, weight=1)
        self._window.grid_rowconfigure(5, weight=1)

        title_lbl = tk.Label(self._window,text="View Tracks",font="TkHeadingFont",bg="#121212",fg="#ff5500",)
        title_lbl.grid(row=0, column=0, columnspan=2, sticky="W", padx=(30, 10), pady=(22, 4))

        subtitle_lbl = tk.Label(self._window,text="Browse the library, inspect details, and play a selected track.",font="TkDefaultFont",bg="#121212",fg="#b8b8b8",)
        subtitle_lbl.grid(row=0, column=2, columnspan=6, sticky="E", padx=(10, 30), pady=(22, 4))

        list_tracks_btn = tk.Button(self._window,text="List All Tracks",command=self._list_tracks_clicked,font="TkDefaultFont",bg="#ff5500",fg="white",activebackground="#d94800",activeforeground="white",relief="flat",bd=0,width=16,)
        list_tracks_btn.grid(row=1, column=0, padx=(30, 10), pady=16, ipady=8, sticky="EW")

        enter_lbl = tk.Label(self._window,text="Enter Track Number",font="TkDefaultFont",bg="#121212",fg="#f5f5f5",)
        enter_lbl.grid(row=1, column=1, columnspan=2, padx=10, pady=16, sticky="E")

        self._input_txt = tk.Entry(self._window,width=8,font="TkDefaultFont",bg="#1e1e1e",fg="#f5f5f5",insertbackground="#ff5500",relief="flat",highlightbackground="#3a3a3a",highlightcolor="#ff5500",highlightthickness=2,)
        self._input_txt.grid(row=1, column=3, padx=10, pady=16, ipady=8, sticky="EW")

        check_track_btn = tk.Button(self._window,text="View Track",command=self._view_tracks_clicked,font="TkDefaultFont",bg="#2a2a2a",fg="#f5f5f5",activebackground="#3a3a3a",activeforeground="white",relief="flat",bd=0,width=14,)
        check_track_btn.grid(row=1, column=4, padx=10, pady=16, ipady=8, sticky="EW")

        library_lbl = tk.Label(self._window,text="Track Library",font="TkHeadingFont",bg="#121212",fg="#f5f5f5",)
        library_lbl.grid(row=2, column=0, columnspan=4, sticky="W", padx=(30, 10), pady=(8, 0))

        choose_image_btn = tk.Button(self._window,text="Choose Image",command=self._choose_image_clicked,font="TkDefaultFont",bg="#2a2a2a",fg="#f5f5f5",activebackground="#3a3a3a",activeforeground="white",relief="flat",bd=0,width=14,)
        choose_image_btn.grid(row=2, column=4, columnspan=2, sticky="EW", padx=(18, 8), pady=(8, 0))

        selected_lbl = tk.Label(self._window,text="Selected Track",font="TkHeadingFont",bg="#121212",fg="#f5f5f5",)
        selected_lbl.grid(row=2, column=6, columnspan=2, sticky="W", padx=(8, 30), pady=(8, 0))

        self._image_lbl = tk.Label(self._window,text="",bg="#1e1e1e",relief="flat",highlightbackground="#3a3a3a",highlightcolor="#ff5500",highlightthickness=2,)
        self._image_lbl.grid(row=3, column=4, columnspan=2, sticky="NSEW", padx=(18, 8), pady=(10, 12))

        self._list_txt = tkst.ScrolledText(self._window,width=72,height=24,wrap="none",font="TkFixedFont",bg="#1e1e1e",fg="#f5f5f5",insertbackground="#ff5500",relief="flat",highlightbackground="#3a3a3a",highlightcolor="#ff5500",highlightthickness=2,)
        self._list_txt.grid(row=3,rowspan=5,column=0,columnspan=4,sticky="NSEW",padx=(30, 15),pady=(10, 20),)

        self._track_txt = tk.Text(self._window,width=42,height=7,wrap="none",font="TkFixedFont",bg="#1e1e1e",fg="#f5f5f5",insertbackground="#ff5500",relief="flat",highlightbackground="#3a3a3a",highlightcolor="#ff5500",highlightthickness=2,)
        self._track_txt.grid(row=3, column=6, columnspan=2, sticky="NSEW", padx=(8, 30), pady=(10, 12))

        self._animation_canvas = tk.Canvas(self._window,width=420,height=165,bg="#181818",highlightbackground="#ff5500",highlightcolor="#ff5500",highlightthickness=2,bd=0,)
        self._animation_canvas.grid(row=4, column=4, columnspan=4, sticky="NSEW", padx=(18, 30), pady=(0, 12))

        play_btn = tk.Button(self._window,text="Play",width=12,command=self._play_track_clicked,font="TkDefaultFont",bg="#ff5500",fg="white",activebackground="#d94800",activeforeground="white",relief="flat",bd=0,)
        play_btn.grid(row=5, column=4, columnspan=2, padx=(18, 8), pady=(0, 10), ipady=10, sticky="EW")

        stop_btn = tk.Button(self._window,text="Stop",width=12,command=self._stop_track_clicked,font="TkDefaultFont",bg="#2a2a2a",fg="#f5f5f5",activebackground="#3a3a3a",activeforeground="white",relief="flat",bd=0,)
        stop_btn.grid(row=5, column=6, columnspan=2, padx=(8, 30), pady=(0, 10), ipady=10, sticky="EW")

        volume_lbl = tk.Label(self._window,text="Volume",font="TkDefaultFont",bg="#121212",fg="#f5f5f5",)
        volume_lbl.grid(row=6, column=4, padx=(18, 8), pady=(4, 0), sticky="E")

        self._volume_value = tk.IntVar(value=70)
        self._volume_scale = tk.Scale(self._window,from_=0,to=100,orient="horizontal",variable=self._volume_value,command=self._volume_changed,font="TkDefaultFont",bg="#121212",fg="#f5f5f5",activebackground="#ff5500",troughcolor="#333333",highlightthickness=0,bd=0,length=360,showvalue=True,)
        self._volume_scale.grid(row=6, column=5, columnspan=3, padx=(0, 30), pady=(4, 0), sticky="EW")

        self._status_lbl = tk.Label(self._window,text="",font="TkDefaultFont",bg="#121212",fg="#b8b8b8",)
        self._status_lbl.grid(row=8, column=0, columnspan=8, sticky="W", padx=30, pady=(0, 18))

        self._list_tracks_clicked()

    def _view_tracks_clicked(self):
        key = self._input_txt.get().strip()
        name = self._library.get_name(key)
        if name is not None:
            artist = self._library.get_artist(key)
            rating = self._library.get_rating(key)
            play_count = self._library.get_play_count(key)
            duration = self._library.get_formatted_duration(key)
            track_details = f"{name}\n{artist}\nrating: {rating}\nplays: {play_count}\nduration: {duration}"
            _set_text(self._track_txt, track_details)
            self._show_track_image(key)
        else:
            _set_text(self._track_txt, f"Track {key} not found")
            self._clear_track_image()
            Popup(self._window, 0, f"Track {key} not found.")
        self._status_lbl.configure(text="View Track button was clicked!")

    def _choose_image_clicked(self):
        key = self._input_txt.get().strip()
        if not key:
            Popup(self._window, 0, "Please enter a track number.")
            self._status_lbl.configure(text="No track number was entered.")
            return

        name = self._library.get_name(key)
        if name is None:
            Popup(self._window, 0, f"Track {key} not found.")
            self._status_lbl.configure(text=f"Track {key} was not found.")
            return

        image_path = filedialog.askopenfilename(parent=self._window,title="Choose track image",initialdir="./assets/imgs",filetypes=[("Image files", "*.png *.gif *.jpg *.jpeg *.bmp"), ("All files", "*.*")])
        if not image_path:
            Popup(self._window, 0, "Image selection was cancelled.")
            self._status_lbl.configure(text="Image selection was cancelled.")
            return

        self._library.set_image_path(key, image_path)
        self._view_tracks_clicked()
        Popup(self._window, 1, f'Image for track "{name}" was updated.')
        self._status_lbl.configure(text=f'Image path for "{name}" was updated.')

    def _clear_track_image(self):
        self._track_image = None
        self._image_lbl.configure(image="", text="")

    def _resolve_image_path(self, raw_path):
        if os.path.isabs(raw_path):
            return os.path.normpath(raw_path)
        return os.path.normpath(os.path.join(os.path.dirname(__file__), raw_path))

    def _show_track_image(self, key):
        raw_path = self._library.get_image_path(key)
        if not raw_path:
            self._clear_track_image()
            return

        image_path = self._resolve_image_path(raw_path)
        if not os.path.exists(image_path):
            self._clear_track_image()
            return

        try:
            self._window.update_idletasks()
            max_width = self._image_lbl.winfo_width() - 8
            max_height = self._image_lbl.winfo_height() - 8
            if max_width < 20:
                max_width = 240
            if max_height < 20:
                max_height = 130
            if Image is not None and ImageTk is not None:
                with Image.open(image_path) as image:
                    image.thumbnail((max_width, max_height))
                    self._track_image = ImageTk.PhotoImage(image.copy())
            else:
                image = tk.PhotoImage(file=image_path)
                scale = max((image.width() + max_width - 1) // max_width, (image.height() + max_height - 1) // max_height, 1)
                self._track_image = image.subsample(scale, scale)
            self._image_lbl.configure(image=self._track_image, text="")
        except (OSError, tk.TclError):
            self._clear_track_image()

    def _list_tracks_clicked(self):
        track_list = self._library.list_all()
        _set_text(self._list_txt, track_list)
        self._status_lbl.configure(text="List Tracks button was clicked!")

    def _play_track_clicked(self):
        key = self._input_txt.get().strip()

        if not key: # number check
            Popup(self._window, 0, "Please enter a track number.")
            self._status_lbl.configure(text="No track number was entered.")
            return

        name = self._library.get_name(key)
        if name is None: # exist song check
            Popup(self._window, 0, f"Track {key} not found.")
            self._status_lbl.configure(text=f"Track {key} was not found.")
            return

        raw_path = self._library.get_path(key)
        if not raw_path: # path check
            Popup(self._window, 0, f'Track {key} does not have an audio file path.')
            self._status_lbl.configure(text=f'Track {key} does not have an audio file path.')
            return

        track_path = os.path.normpath(os.path.join(os.path.dirname(__file__), raw_path))
        if not os.path.exists(track_path): # file exists check
            Popup(self._window, 0, f'Audio file for track {key} was not found.')
            self._status_lbl.configure(text=f'Audio file for track {key} was not found.')
            return

        if pygame is None: # pygame import failsafe handle
            Popup(self._window, 0, "pygame is not installed, so audio playback is unavailable.")
            self._status_lbl.configure(text="pygame is not installed.")
            return

        try: # pygame mixer engine failsafe handle
            if not self._mixer_ready:
                pygame.mixer.init()
                self._mixer_ready = True

            pygame.mixer.music.load(track_path)
            pygame.mixer.music.set_volume(self._volume_scale.get() / 100)
            pygame.mixer.music.play()
            self._library.increment_play_count(key)
        except pygame.error as error:
            Popup(self._window, 0, f"Unable to play track {key}: {error}")
            self._status_lbl.configure(text=f"Unable to play track {key}.")
            return
        
        self._view_tracks_clicked()
        
        try: # animation failsafe handle
            self._start_visualizer()
        except Exception as error:
            self._status_lbl.configure(text="Audio visualizer failed to start.")
            return

        self._status_lbl.configure(text=f'Now playing "{name}".')

    def _stop_track_clicked(self):
        if pygame is None or not self._mixer_ready:
            self._status_lbl.configure(text="No track is currently playing.")
            Popup(self._window, 0, "No track is currently playing.")
            return

        pygame.mixer.music.stop()

        try: # animation failsafe handle
            self._stop_visualizer()
        except Exception as error:
            self._status_lbl.configure(text="Audio visualizer failed to stop.")
            return

        self._status_lbl.configure(text="Playback stopped.")
        Popup(self._window, 1, "Playback stopped.")

    def _volume_changed(self, value):
        volume = float(value) / 100
        if pygame is not None and self._mixer_ready:
            try:
                pygame.mixer.music.set_volume(volume)
            except pygame.error:
                return

        if hasattr(self, "_status_lbl"):
            self._status_lbl.configure(text=f"Volume set to {int(float(value))}%.")

    def _start_visualizer(self):
        self._bars = 40
        self._canvas_width = 660
        self._canvas_height = 165
        self._bar_width = self._canvas_width // self._bars
        self._visualizer_running = True
        self._animate_visualizer()

    def _animate_visualizer(self):
        if not self._visualizer_running:
            return
    
        self._animation_canvas.delete("bars")
    
        center_y = self._canvas_height // 2
    
        for i in range(self._bars):
            height = random.randint(3, self._volume_value.get() + 3)
    
            x1 = i * self._bar_width
            x2 = x1 + self._bar_width - 2
    
            y1 = center_y - height
            y2 = center_y + height
    
            color = random.choice([
                "#ff5500",
                "#ff7733",
                "#ffaa66",
                "#ffd1b3"
            ])
    
            self._animation_canvas.create_rectangle(
                x1, y1, x2, y2,
                fill=color,
                outline="",
                tags="bars"
            )
    
        self._window.after(70, self._animate_visualizer)

    def _stop_visualizer(self):
        self._visualizer_running = False
        self._animation_canvas.delete("bars")

if __name__ == "__main__":  # only runs when this file is run as a standalone
    window = tk.Tk()        # create a TK object
    fonts.configure()       # configure the fonts
    library = _build_library()
    TrackViewer(window, library)     # open the TrackViewer GUI
    window.mainloop()       # run the window main loop, reacting to button presses, etc
