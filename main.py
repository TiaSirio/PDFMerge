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

location = []
finalLocation = './Merged/MergedPdf.pdf'
pdfFile = []
pdfReader = []
filePaths = []
endingPath = []
tempString = ""
fileToDelete = []

print("Choose the files in order of merging.")

actualPath = pathlib.Path().resolve()

tk.Tk().withdraw()
filez = fd.askopenfilenames(title='Choose a file', initialdir=actualPath)

print(filez)

for f in filez:
    filePaths.append(str(f))

for f in filePaths:
    if f.endswith(".png") or f.endswith("jpg") or f.endswith("jpeg"):
        tempString = f
        while tempString[:-1] != ".":
            tempString = tempString[:-1]
            if tempString.endswith("."):
                break
        tempString = tempString + "pdf"
        image = Image.open(f)
        pdf_bytes = img2pdf.convert(image.filename)
        file = open(tempString, "wb")
        file.write(pdf_bytes)
        image.close()
        file.close()
        index = filePaths.index(f)
        filePaths = filePaths[:index] + [tempString] + filePaths[index + 1:]
        fileToDelete.append(tempString)
    elif f.endswith(".docx") or f.endswith("doc"):
        tempString = f
        while tempString[:-1] != ".":
            tempString = tempString[:-1]
            if tempString.endswith("."):
                break
        tempString = tempString + "pdf"
        convert(f, tempString)
        index = filePaths.index(f)
        filePaths = filePaths[:index] + [tempString] + filePaths[index + 1:]
        fileToDelete.append(tempString)
    elif f.endswith(".txt"):
        tempString = f
        while tempString[:-1] != ".":
            tempString = tempString[:-1]
            if tempString.endswith("."):
                break
        tempString = tempString + "pdf"
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        fTxt = open(f, "r")
        for x in fTxt:
            pdf.cell(200, 10, txt=x, ln=1, align='L')
        pdf.output(tempString)
        index = filePaths.index(f)
        filePaths = filePaths[:index] + [tempString] + filePaths[index + 1:]
        fileToDelete.append(tempString)

for f in filePaths:
    location.append(f)

if not len(filePaths):
    raise Exception("No PDF selected.")
else:
    Path(str(actualPath) + "/Merged").mkdir(parents=True, exist_ok=True)

for x in location:
    pdfFileTemp = open(x, 'rb')
    pdfFile.append(pdfFileTemp)

for x in pdfFile:
    pdfReaderTemp = PyPDF2.PdfFileReader(x)
    pdfReader.append(pdfReaderTemp)

pdfWriter = PyPDF2.PdfFileWriter()

for x in pdfReader:
    for pageNum in range(x.numPages):
        pageObj = x.getPage(pageNum)
        pdfWriter.addPage(pageObj)

pdfOutputFile = open(finalLocation, 'wb')
pdfWriter.write(pdfOutputFile)
pdfOutputFile.close()

for x in pdfFile:
    x.close()

for f in fileToDelete:
    os.remove(f)
