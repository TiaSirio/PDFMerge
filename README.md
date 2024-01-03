# PDFMerge 📑

## Overview 🌐
PDFMerge is a Python program that allows you to merge multiple PDF files into one single PDF document.

## Requirements 📝

The following libraries are required to run PDFMerge:

```python
import PyPDF2
import tkinter as tk
import tkinter.filedialog as fd
import pathlib
from pathlib import Path
import img2pdf
from PIL import Image
from docx2pdf import convert
from fpdf import FPDF
import os
```

## Install requirements 🛜
To install the required libraries, run the following command:

```
pip install PyPDF2 tkinter pathlib img2pdf Pillow docx2pdf fpdf
```

## Usage 🖥️

To use PDFMerge, run the main.py script. If the libraries are installed in a venv, follow the instruction in the file "execute.txt".

To merge files:

- Select the files in the file explorer and click "Open".
- The new merged PDF will be created in the project directory.

You can also merge other file formats, such as DOCX, images and txt.

## Author 🧑🏻‍💻

- Mattia Siriani