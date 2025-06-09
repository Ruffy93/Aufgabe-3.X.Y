import tkinter as tk
from tkinter import ttk, filedialog
import fitz  # PyMuPDF

class PDFViewerTab:
    def __init__(self, notebook):
        self.tab = ttk.Frame(notebook)
        notebook.add(self.tab, text="📄 PDF Viewer")

        self.text = tk.Text(self.tab, wrap="word", height=30, width=80)
        self.text.pack(expand=True, fill='both')

        controls = tk.Frame(self.tab)
        controls.pack()

        tk.Button(controls, text="PDF laden", command=self.load_pdf).pack(side=tk.LEFT)
        tk.Button(controls, text="◀️", command=self.prev_page).pack(side=tk.LEFT)
        tk.Button(controls, text="▶️", command=self.next_page).pack(side=tk.LEFT)

        self.pdf_doc = None
        self.page_number = 0

    def load_pdf(self):
        file_path = filedialog.askopenfilename(filetypes=[("PDF Dateien", "*.pdf")])
        if file_path:
            self.pdf_doc = fitz.open(file_path)
            self.page_number = 0
            self.show_page()

    def show_page(self):
        if self.pdf_doc:
            page = self.pdf_doc.load_page(self.page_number)
            text = page.get_text()
            self.text.delete("1.0", tk.END)
            self.text.insert(tk.END, text)

    def prev_page(self):
        if self.pdf_doc and self.page_number > 0:
            self.page_number -= 1
            self.show_page()

    def next_page(self):
        if self.pdf_doc and self.page_number < len(self.pdf_doc) - 1:
            self.page_number += 1
            self.show_page()