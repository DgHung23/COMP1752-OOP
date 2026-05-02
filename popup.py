import tkinter as tk


class Popup:
    def __init__(self, parent, popup_type, message):
        self._parent = parent
        self._popup_type = popup_type
        self._message = message

        self._window = tk.Toplevel(parent)
        self._build_UI()
        self._center_window()

        # popup place on top of parent window
        self._window.transient(self._parent)

        # prevent interaction with parent window
        self._window.grab_set()

        # set focus to popup
        self._window.focus_force()

        # make topup appear above all windows
        self._window.attributes("-topmost", True)
        self._window.after(100, lambda: self._window.attributes("-topmost", False))

    def _build_UI(self):
        self._window.geometry("360x170")
        self._window.resizable(False, False)
        self._window.title("Notification")
        self._window.grid_columnconfigure(0, weight=1)
        if self._popup_type == 1:
            title_text = "Success"
            title_color = "#00ff26"
            btn_color = "#00cc1a"
        else:
            title_text = "Error"
            title_color = "#ff3333"
            btn_color = "#cc0000"

        self._window.configure(bg="#121212")

        title_label = tk.Label(self._window,text=title_text,font=("Arial", 16, "bold"),bg="#121212",fg=title_color)
        title_label.grid(row=0, column=0, padx=24, pady=(22, 8), sticky="W")

        message_label = tk.Label(self._window,text=self._message,font=("Arial", 12),bg="#121212",fg="#ff8554",wraplength=310,justify="center")
        message_label.grid(row=1, column=0, padx=24, pady=(0, 18), sticky="NSEW")

        close_button = tk.Button(self._window,text="Close",command=self._close_popup,font=("Arial", 10, "bold"),bg=btn_color,fg="white",activebackground="#d94800",activeforeground="white",relief="flat",bd=0,width=10)
        close_button.grid(row=2, column=0, padx=24, pady=(0, 18), ipady=6, sticky="E")

    def _center_window(self):
        self._window.update_idletasks()

        width = self._window.winfo_width()
        height = self._window.winfo_height()

        parent_x = self._parent.winfo_x()
        parent_y = self._parent.winfo_y()
        parent_width = self._parent.winfo_width()
        parent_height = self._parent.winfo_height()

        x = parent_x + (parent_width // 2) - (width // 2)
        y = parent_y + (parent_height // 2) - (height // 2)

        self._window.geometry(f"{width}x{height}+{x}+{y}")

    def _close_popup(self):
        self._window.grab_release()
        self._window.destroy()


if __name__ == "__main__": # standalone run for testing the popup
    root = tk.Tk()
    root.title("popup standalone run")
    root.geometry("300x200")


    btn1 = tk.Button(root, text="Success", width=15, height=5 , command= lambda: Popup(root, 1, "this is a success message"))
    btn1.grid(row=0, column=0, pady=50, padx=10)

    btn2 = tk.Button(root, text="Error", width=15, height=5, command= lambda: Popup(root, 0, "this is an error message"))
    btn2.grid(row=0, column=1, pady=50, padx=10)

    root.mainloop()
