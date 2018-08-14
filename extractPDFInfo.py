# -*- coding: utf-8 -*-
"""
Created on Thu Apr 19 10:25:50 2018

@author: daniel.scott
"""
import pdfreader, pyocr

import PyPDF2
pdfFileObj = open(r'C:\Users\daniel.scott\Desktop\pdf renaming\test\RGCH1994_v21N2pp197_212_Cerro_Iman_1994.pdf, 'rb')
C:\Users\daniel.scott\Desktop\pdf renaming\test

import os
from pdfrw import PdfReader

path = r'C:\Users\daniel.scott\Desktop\pdf renaming\test'


def renameFileToPDFTitle(path, fileName):
    fullName = os.path.join(path, fileName)
    # Extract pdf title from pdf file
    newName = PdfReader(fullName).Info.Title
    # Remove surrounding brackets that some pdf titles have
    newName = newName.strip('()') + '.pdf'
    newFullName = os.path.join(path, newName)
    os.rename(fullName, newFullName)


for fileName in os.listdir(path):
    # Rename only pdf files
    fullName = os.path.join(path, fileName)
    if (not os.path.isfile(fullName) or fileName[-4:] != '.pdf'):
        continue
    renameFileToPDFTitle(path, fileName)
    
    
####to get doc information put in code below
from PyPDF2 import PdfFileReader
inputPdf = PdfFileReader(open(r'C:\Users\daniel.scott\Desktop\pdf renaming\test\RGCH1994_v21N2pp197_212_Cerro_Iman_1994.pdf', "rb"))
docInfo = inputPdf.getDocumentInfo()
docInfo.author
docInfo.creator
docInfo.title
docInfo.subject




from PyPDF2 import PdfFileReader
import os,json

# Get all the PDF filenames.
pdfFiles = []
path = r'Q:\06_Library'

for dirpath, dirnames, files in os.walk(path):
    for filename in files:
        if filename.endswith(".pdf"):
            pdfFiles.append(filename)

pdfFiles.sort(key=str.lower)
outfile = r"C:\Users\daniel.scott\Desktop\pdf renaming\Index.txt"
# Loop through all the PDF files.
for filename in pdfFiles:
    try:
        inputPdf = PdfFileReader(open(filename, "rb"))
        docInfo = inputPdf.getDocumentInfo()
        with open(outfile, 'a') as f:
            json.dump("PDF Name: " + filename, f, ensure_ascii=False)
        with open(outfile, 'a') as f:
            json.dump("PDF Title: " + docInfo.title, f, ensure_ascii=False)
        with open(outfile, 'a') as f:
            json.dump("PDF Author: " + docInfo.author, f, ensure_ascii=False)
        with open(outfile, 'a') as f:
            json.dump("--------------------------------", f, ensure_ascii=False)
        
    except:
        with open(outfile, 'a') as f:
            json.dump("unable to open " + filename, f, ensure_ascii=False)
        pass
# TODO: Loop through all the pages (except the 
inputPdf = PdfFileReader(open(r'C:\Users\daniel.scott\Desktop\pdf renaming\test\RGCH1994_v21N2pp197_212_Cerro_Iman_1994.pdf', "rb"))
docInfo = inputPdf.getDocumentInfo()
docInfo.author
docInfo.creator
docInfo.title
docInfo.subject