from .document_generator import generate_word_doc, preview_latest_doc
from .file_manager import FolderSelect
from .text_extraction import get_files_in_directory
import tkinter as tk
import ttkbootstrap as ttk
from tkinter import scrolledtext


class AutomationApp(tk.Tk):
    """
    Main application class for the PDF Data Extraction Automation Tool.
    This application allows the user to select a folder containing PDF files,
    generate a Word document with guest information, and view a preview of the generated document.
    """

    def __init__(self):
        """
        Initializes the application window, sets up UI components, and creates the layout.
        """
        super().__init__()
        self.title("PDF Data Extraction - Automation")
        self.geometry("900x600")
        self.minsize(width=700, height=400)

        self._create_widgets()

    def _create_widgets(self):
        """
        Initializes all UI components (tabs, buttons, text areas) and arranges them in the layout.
        """
        # Create a Notebook (Tabbed Interface)
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # Create Main Tab (For selecting folders and generating documents)
        self.main_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.main_tab, text="Main")

        ttk.Label(self.main_tab, text="PDF Data Extraction - Automation", font="Calibri 24 bold").pack()

        self.directory_selector = FolderSelect(self.main_tab, "Select Guest Folder", self.update_file_list)
        self.directory_selector.pack(padx=15, pady=5)

        ttk.Button(self.main_tab, text="Generate Guest Info File", command=self.generate_guest_info_file).pack(padx=15, pady=5)

        # File list display
        self.file_listbox = tk.Listbox(self.main_tab, height=10, width=40)
        self.file_listbox.pack(padx=15, pady=5)
        self.file_listbox.pack_forget()  # Hide the file listbox initially

        # Create Preview Tab
        self.preview_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.preview_tab, text="Preview")

        ttk.Label(self.preview_tab, text="Document Preview:").pack(anchor="w")
        self.preview_text = scrolledtext.ScrolledText(self.preview_tab, wrap=tk.WORD, font=("Courier", 10))
        self.preview_text.pack(fill=tk.BOTH, expand=True)

    def generate_guest_info_file(self):
        """
        Generates the guest information Word document from the PDF files in the selected folder
        and extracts the guest information summary table from the Word document so it can be 
        previewed in the application window.
        """
        self.folder_path = self.directory_selector.folder_selected
        if not self.folder_path:
            print("No folder selected.")  # Could replace with a UI alert
            return

        #Generates word document with summary tables containing guest information
        generate_word_doc(folder_path=self.folder_path)

        #Extract the tables from Word document and populates the preview window
        preview_latest_doc(folder_path=self.folder_path, preview_text=self.preview_text)

    def update_file_list(self, folder_path, ext='.pdf'):
        """
        Updates the Listbox widget with the list of files in the selected folder.
        
        Args:
            folder_path (str): The path of the selected folder.

        """
        if folder_path:
            files = get_files_in_directory(folder_path, ext=ext)
            # Clear the current list
            self.file_listbox.delete(0, tk.END)  

            #Repopulate preview list
            for file in files:
                self.file_listbox.insert(tk.END, file)  
            
            # Show the file listbox after folder is selected
            self.file_listbox.pack()  

