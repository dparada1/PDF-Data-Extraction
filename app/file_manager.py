from .constants import INITIALDIR
from .utils import shorten_path
import tkinter as tk
import ttkbootstrap as ttk
from tkinter import filedialog, StringVar


class FolderSelect(ttk.Frame):
    """
    Custom widget to allow the user to select a folder from the filesystem and display only
    the last 3 directories in the path while maintaining the full path internally.
    """

    def __init__(self, parent, label_text="", update_file_list_callback=None):
        """
        Initializes the folder selection widget.

        Args:
            parent (tk.Widget): The parent widget to attach this frame to.
            label_text (str): The label text to be displayed next to the folder path entry.
            update_file_list_callback (function): Callback to update the list of files in the UI when a folder is selected.
        """
        super().__init__(parent)
        self.folder_path_var = StringVar()
        self.update_file_list_callback = update_file_list_callback

        ttk.Label(self, text=label_text).grid(row=0, column=0)
        ttk.Entry(self, textvariable=self.folder_path_var, width=40).grid(row=0, column=1)
        ttk.Button(self, text="Browse", command=self._browse_folder).grid(row=0, column=2, padx=15, pady=10)

    def _browse_folder(self, initialdir=INITIALDIR):
        """
        Opens a folder selection dialog to choose a directory and updates the folder path.
        It displays only the last 3 levels of the path.
        """
        self.folder_selected = filedialog.askdirectory(initialdir=initialdir)
        # shortened_path = self._shorten_path(self.folder_selected)
        self.folder_path_var.set(shorten_path(self.folder_selected))
        
        # Call the callback to update the file list
        if self.update_file_list_callback:
            self.update_file_list_callback(self.folder_selected)

    @property
    def folder_path(self):
        """
        Returns the current folder path selected by the user.

        Returns:
            str: The folder path.
        """
        return self.folder_path_var.get()
    
