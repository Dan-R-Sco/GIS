# -*- coding: utf-8 -*-
"""
Created on Thu Apr 19 10:25:50 2018
Script that indexes all of the pdf's that are in a folder and writes into txt file
@author: daniel.scott
"""

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
#determine the output txt file
outfile = <OUTPUTFILE>
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
inputPdf = PdfFileReader(open(<DIRECTORY AND FILE>, "rb"))
docInfo = inputPdf.getDocumentInfo()
docInfo.author
docInfo.creator
docInfo.title
docInfo.subject



##another method
import os
from pdfrw import PdfReader
#define patht hat holds the pdfs i.e.r'C:\Dan'
path = <ENTER PATH>

def renameFileToPDFTitle(path, fileName):
    fullName = os.path.join(path, fileName)
    # Extract pdf title from pdf file
    newName = PdfReader(fullName).Info.Title
    # Remove surrounding brackets that some pdf titles have
    newName = newName.strip('()') + '.pdf'
    newFullName = os.path.join(path, newName)
    os.rename(fullName, newFullName)

#rename the file to the metadata title
for fileName in os.listdir(path):
    # Rename only pdf files
    fullName = os.path.join(path, fileName)
    if (not os.path.isfile(fullName) or fileName[-4:] != '.pdf'):
        continue
    renameFileToPDFTitle(path, fileName)
    
    
####to get doc information put in code below
from PyPDF2 import PdfFileReader
inputPdf = PdfFileReader(open(<DIRECTORY>, "rb"))
docInfo = inputPdf.getDocumentInfo()
docInfo.author
docInfo.creator
docInfo.title
docInfo.subject



