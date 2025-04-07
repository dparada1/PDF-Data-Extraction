import os
import docx
import tkinter as tk
from prettytable import PrettyTable
from .text_extraction import GuestDocumentGenerator, get_files_in_directory


def generate_word_doc(folder_path):
    """
    Calls function that extracts all the customer forms in the given folder_path and then calls 
    another function that creates a word document with every customer's information.
    """
    guest_document = GuestDocumentGenerator(file_path=folder_path)
    guest_files = get_files_in_directory(directory=folder_path, ext=".pdf")
    guest_document.generate_document(guest_files=guest_files)


def get_latest_word_doc(folder_path):
    """
    Finds and returns the most recently created Word document containing 'Guest Info' in the filename.

    Args:
        folder_path (str): The directory path where Word documents are stored.

    Returns:
        str or None: The full path of the latest Word document if found, otherwise None.
    """
    word_docs = [f for f in os.listdir(folder_path) if f.endswith(".docx") and "Guest Info" in f]
    if not word_docs:
        return None

    latest_doc = max(word_docs, key=lambda f: os.path.getctime(os.path.join(folder_path, f)))
    return os.path.join(folder_path, latest_doc)


def extract_tables_from_doc(doc_path):
    """
    Extracts tables from a Word document and formats them as PrettyTable objects.

    Args:
        doc_path (str): The full path of the Word document to extract tables from.

    Returns:
        list: A list of formatted table strings or an error message if the document cannot be read.
    """
    try:
        doc = docx.Document(doc_path)
        tables_text = []

        for table in doc.tables:
            pretty_table = format_table(table)
            tables_text.append(pretty_table.get_string(hrules=1))  # Add horizontal rules for clarity
            tables_text.append("\n---\n")  # Separator between tables

        return tables_text
    except Exception as e:
        return [f"Error loading document: {e}"]


def format_table(table):
    """
    Formats a Word document table into a PrettyTable object for better readability.

    Args:
        table (docx.table.Table): A table extracted from a Word document.

    Returns:
        PrettyTable: A PrettyTable object containing the extracted table data.
    """
    pretty_table = PrettyTable()
    pretty_table.max_width = 10  # Reduce column width for better visibility
    pretty_table.border = True  # Ensure borders for clear table separation
    pretty_table.padding_width = 1  # Minimize column padding

    headers, seen_headers = [], set()
    for i, cell in enumerate(table.rows[0].cells):
        header = cell.text.strip()
        if header in seen_headers:
            header = f"{header}_{i}"  # Ensure unique headers
        seen_headers.add(header)
        headers.append(header)

    pretty_table.field_names = headers

    for row in table.rows[1:]:
        row_data = [cell.text.strip() for cell in row.cells]
        pretty_table.add_row(row_data)

    return pretty_table


def preview_latest_doc(folder_path, preview_text):
    """
    Displays a preview of the most recently generated Word document's tables in a ScrolledText widget.

    Args:
        folder_path (str): The folder path where the generated Word documents are stored.
        preview_text (tkinter.scrolledtext.ScrolledText): The text widget to display the extracted table data.

    Returns:
        None
    """
    preview_text.delete("1.0", tk.END)

    latest_doc_path = get_latest_word_doc(folder_path)
    if not latest_doc_path:
        preview_text.insert(tk.END, "No Word document found.")
        return

    tables_text = extract_tables_from_doc(latest_doc_path)
    preview_text.insert(tk.END, f"Preview of {os.path.basename(latest_doc_path)} (Tables Only):\n\n")
    preview_text.insert(tk.END, "\n".join(tables_text))
