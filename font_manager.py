import tkinter.font as tkfont


def configure():
    ui_family = "Segoe UI"
    monospace_family = "Consolas"

    default_font = tkfont.nametofont("TkDefaultFont")
    default_font.configure(size=15, family=ui_family)

    fixed_font = tkfont.nametofont("TkFixedFont")
    fixed_font.configure(size=15, family=monospace_family)
