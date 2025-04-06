# PDF Data Extraction Automation Tool

## Overview
The **PDF Data Extraction Automation Tool** is a Tkinter-based application that automates the extraction of guest information from PDF files and generates Word documents. It features a user-friendly interface to select a folder, preview extracted data, and manage document generation efficiently.

## Features
- Select a folder containing PDF files.
- Maintains the absolute path internally but displays only the last three levels of the selected folder.
- Display a list of files in the selected folder.
- Generate a Word document with extracted guest information.
- Preview tables from the most recently generated Word document.
- Tab for document preview.


## Project Structure
The project is modularized for maintainability and scalability:

```
PDF_Data_Extraction_Automation_Tool/
.
├── README.md                             # Project documentation
├── app
│   ├── constants.py                      # Contains global variable constants
│   ├── document_generator.py             # Extracts PDF data, generates Word documents and file preview
│   ├── file_manager.py                   # Manages file selection and listing
│   ├── gui.py                            # Handles UI components and event management
│   ├── text_extraction
│   │   ├── __init__.py                   # Initializes package by importing various components
│   │   ├── checkmark_utils.py            # Processes checkmarks in PDF forms
│   │   ├── constants.py                  # Contains global variable constants
│   │   ├── containers.py                 # Defines various data structures used
│   │   ├── data_extraction.py            # Contains the logic to extract data from PDF
│   │   ├── formatting_utils.py           # Contains utility functions for formatting Word document
│   │   ├── prompt_response_mapping.py    # Maps prompts to customer responses
│   │   ├── utils.py                      # Contains additional utility functions
│   │   └── word_doc.py                   # Contains the logic to create Word documents
│   └── utils.py                          # Contains utility functions for formatting and processing
├── main.py                               # Entry point of the application
├── requirements.txt                      # Required packages for this project
└── sample_forms                          # Folder for sample PDF forms
```

## Modules
### 1. `main.py`
The entry point of the application, initializing the GUI and starting the main event loop.

### 2. `gui.py`
Handles the graphical user interface using **Tkinter** and **ttkbootstrap**. It includes:
- Folder selection widget (`FolderSelect`).
- File listing (`Listbox` widget).
- Buttons to generate documents and toggle previews.
- Scrolled text area for document previews.

### 3. `file_manager.py`
Responsible for:
- Fetching the list of files from the selected folder.
- Displaying files in a `Listbox`.

### 4. `document_generator.py`
Handles document processing:
- Extracts guest information from PDFs.
- Generates Word documents using `python-docx`.
- Extracts tables from Word documents for preview.

### 5. `utils.py`
Contains utility functions for:
- Managing file path processing (e.g., shortening to the last three directories).
- Extracts files with a given extension from a given directory.

### 6. `data_extraction.py`
Handles document processing:
- Extracts guest information from PDFs.

### 7. `word_doc.py`
Contains utility functions for:
- Creates Word document and populates it.

### 8. `formatting_utils.py`
Contains utility functions for:
- Formatting extracted data.
- Formatting cells in Word document.

## Installation
### Prerequisites
Ensure you have Python installed (>=3.7). Install required dependencies:

```sh
pip3 install -r requirements.txt
```

## Usage
1. Run the application:
   ```sh
   python3 main.py
   ```
2. Select a folder containing PDFs.
3. Click **"Generate Guest Info File"** to create a Word document.
4. Click **"Show/Hide Preview"** to view extracted tables.

## APP creation
You can also turn this code into an app with an icon using PyInstaller

1. Install PyInstaller:
   ```sh
   pip install pyinstaller
   ```
2. Create an executable with an icon:
   ```sh
   python3 -m PyInstaller your_python_file.py --onefile -w --name "name_of_the_application"
   ```
3. Go to the dist folder and double click on the application icon

## Future Improvements
- Implement error handling for unsupported file types.
- Support additional document formats.
- Add more customization options for table extraction.

## License
MIT License.

