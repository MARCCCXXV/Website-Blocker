import tkinter as tk

class FocusAppBlocker:
    def __init__(self,root):
        root.geometry("300x300")
        root.configure(bg= "#32a852")

root = tk.Tk()
app = FocusAppBlocker(root)
root.mainloop()