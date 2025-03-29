from tkinter import *

# Window's properties
root = Tk()
root.geometry("1000x600")

# Global variables
panel_x = -320
show_panel_x = 0


# Functions used to create the animation
def open_panel():
    global panel_x
    global show_panel_x
    if panel_x < 0:
        panel_x += 5
        panel.place(x=panel_x, y=0)
        show_panel_x += 5
        show_panel.place(x=show_panel_x, y=260)
        if panel_x >= 0:
            show_panel.configure(command=close_panel)
            show_panel.configure(text="<<")
        else:
            root.after(5, open_panel)


def close_panel():
    global panel_x
    global show_panel_x
    panel_x -= 5
    panel.place(x=panel_x, y=0)
    show_panel_x -= 5
    show_panel.place(x=show_panel_x, y=260)
    if panel_x <= -320:
        show_panel.configure(command=open_panel)
        show_panel.configure(text=">>")
    else:
        root.after(5, close_panel)


# Widgets
panel = Frame(root, width=320, height=600, bg="green", relief="flat")
panel.place(x=-320, y=0)

show_panel = Button(root, text=">>", font=("Bold", 17), bg="green",
                    fg="white", command=open_panel)

show_panel.place(x=0, y=260)

root.mainloop()