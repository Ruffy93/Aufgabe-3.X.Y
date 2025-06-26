import tkinter as tk
from controller.haushaltsbuch_controller import HaushaltsbuchController

def main():
    root = tk.Tk()
    app = HaushaltsbuchController(root)
    root.mainloop()

if __name__ == "__main__":
    main() 