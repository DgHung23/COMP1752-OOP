import tkinter as tk


class Popup:
    def __init__(self, parent, popup_type, message):
        self.parent = parent
        self.popup_type = popup_type
        self.message = message

        self.window = tk.Toplevel(parent)
        self.window.resizable(False, False)
        self.window.title("Notification")

        self._setup_ui()
        self._center_window()

        # popup place on top of parent window
        self.window.transient(self.parent)

        # prevent interaction with parent window
        self.window.grab_set()

        # set focus to popup
        self.window.focus_force()

        # make topup appear above all windows
        self.window.attributes("-topmost", True)
        self.window.after(100, lambda: self.window.attributes("-topmost", False))

    def _setup_ui(self):
        if self.popup_type == 1:
            title_text = "✔ success"
            bg_color = "#4CAF50"
        else:
            title_text = "✘ error"
            bg_color = "#F44336"

        self.window.configure(bg=bg_color)

        frame = tk.Frame(self.window, bg=bg_color, padx=20, pady=15)
        frame.grid(row=0, column=0)

        title_label = tk.Label(
            frame,
            text=title_text,
            font=("Arial", 14, "bold"),
            bg=bg_color,
            fg="white"
        )
        title_label.grid(row=0, column=0, pady=(0, 8), sticky="w")

        message_label = tk.Label(
            frame,
            text=self.message,
            font=("Arial", 11),
            bg=bg_color,
            fg="white",
            wraplength=300,
            justify="center"
        )
        message_label.grid(row=1, column=0, pady=(0, 40))

        close_button = tk.Button(
            frame,
            text="Close",
            command=self.close_popup,
            font=("Arial", 10, "bold"),
            padx=10,
            pady=3
        )
        close_button.grid(row=2, column=0, sticky="e")

    def _center_window(self):
        self.window.update_idletasks()

        width = self.window.winfo_width()
        height = self.window.winfo_height()

        parent_x = self.parent.winfo_x()
        parent_y = self.parent.winfo_y()
        parent_width = self.parent.winfo_width()
        parent_height = self.parent.winfo_height()

        x = parent_x + (parent_width // 2) - (width // 2)
        y = parent_y + (parent_height // 2) - (height // 2)

        self.window.geometry(f"{width}x{height}+{x}+{y}")

    def close_popup(self):
        self.window.grab_release()
        self.window.destroy()


if __name__ == "__main__": # standalone run for testing the popup
    root = tk.Tk()
    root.title("popup standalone run")
    root.geometry("300x200")


    btn1 = tk.Button(root, text="Success", width=15, height=5 , command= lambda: Popup(root, 1, "this is a success message"))
    btn1.grid(row=0, column=0, pady=50, padx=10)

    btn2 = tk.Button(root, text="Error", width=15, height=5, command= lambda: Popup(root, 0, "this is an error message"))
    btn2.grid(row=0, column=1, pady=50, padx=10)

    root.mainloop()