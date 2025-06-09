import tkinter as tk
from tkinter import ttk
from pdf_viewer import PDFViewerTab
from backup_tool import BackupTab
from onboarding_tool import OnboardingTab

class MultiToolApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Tools")
        self.root.geometry("800x600")

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True)

        PDFViewerTab(self.notebook)
        BackupTab(self.notebook)
        OnboardingTab(self.notebook)

if __name__ == "__main__":
    root = tk.Tk()
    app = MultiToolApp(root)
    root.mainloop()