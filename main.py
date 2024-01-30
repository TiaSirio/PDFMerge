import sys
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


def Selector(data):
    def append(widget, element, results, display):
        # append element to list
        results.append(element)

        # disable button
        widget['state'] = 'disabled'

        # add element to label
        current = display['text']
        if current:
            current += '\n'
        display['text'] = current + element

    # create window
    root = tk.Tk()

    # list for correct order
    results = []

    # label to display order
    tk.Label(root, text='Select the files in the desired order').pack()
    l = tk.Label(root, anchor='w', justify='left')
    l.pack(fill='x')

    # buttons to select elements
    tk.Label(root, text='Files to select').pack()

    for d in data:
        b = tk.Button(root, text=d, anchor='w')
        b['command'] = lambda w=b, e=d, r=results, d=l: append(w, e, r, d)
        b.pack(fill='x')

    # button to close window
    b = tk.Button(root, text='Close', command=root.destroy)
    b.pack(fill='x', pady=(15, 0))

    # start mainloop
    root.mainloop()

    return results


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

root = tk.Tk()
root.withdraw()
filez = fd.askopenfilenames(parent=root, title='Choose your files', initialdir=actualPath)
root.destroy()

if len(filez) == 0:
    print("No file Selected.")
    sys.exit(1)

filez = Selector(filez)
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
    pdfReaderTemp = PyPDF2.PdfReader(x)
    pdfReader.append(pdfReaderTemp)

pdfWriter = PyPDF2.PdfWriter()

for x in pdfReader:
    for pageNum in range(len(x.pages)):
        pageObj = x.pages[pageNum]
        pdfWriter.add_page(pageObj)

pdfOutputFile = open(finalLocation, 'wb')
pdfWriter.write(pdfOutputFile)
pdfOutputFile.close()

for x in pdfFile:
    x.close()

for f in fileToDelete:
    os.remove(f)
