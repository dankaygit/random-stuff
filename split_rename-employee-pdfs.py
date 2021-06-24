#!/usr/bin/env python

import os
from PyPDF2 import PdfFileWriter, PdfFileReader

# Does this script run with user input or not?
# If yes, set to True.

interactive = False

#Info about the PDF we need to edit

## Get all pdfs from the "source" directory and put the file names in a list called input_files
input_files = [file for file in os.listdir("source") if file.endswith(".pdf")]
## Delete the ".pdf" extension for every file name so we can now extract the available info from each file name
files = [file.strip(".pdf") for file in input_files]
## Split up the name by separating everything before and after each "_". This returns a list of split up strings for each initial string.
## Here it's important that we already have an idea of what our input will look like. In our sample files we have the format FileName_Year_Month_IDN.pdf. Assuming this to be our input, we can extract year and month from our files.
files = [file.split("_") for file in files]


# Either get the employee names interactively (through user input) or extract them from some saved file called employees.txt (since there is just quick and dirty, we assume a txt file with one employee name per line, no tabs or ws.) It's important that the employee names come up in the same order as they are in the input pdf files.

employees = []
sep = "_"

## Extract all names from the file and clean up line breaks
if not interactive:
    with open("source/employees.txt", "r") as file:
        lines = file.readlines()
        lines = [line.strip("\n") for line in lines]
        employees = lines
    
    ## Clean up empty lines, so we don't have "employees" which have no name due to empty lines in the file.
    employees = [employee for employee in employees if employee not in ["\n", "", " "]]

else:
    print("Please input in one line all employees in the order as they appear in the the input document, separated by a " + sep + " \nFor example: Bob" + sep + "Alice" + sep + "Brian" + sep + "Dora" + sep + "Charlie \n")
    
    print("Please input all employees as described above: ")

    employees = input()
    employees = employees.split(sep)

print(employees)

## Here we start the splitting process.

## We take each input file from input_files and create subdirectories in a new "output" based on the file name
for input_file in input_files:

    fileName = input_file.strip(".pdf")
    output_dir = os.getcwd() + "/output/" + fileName + "/"
    if fileName in os.listdir("output"): 
        raise Exception ("It seems like " + fileName + " has already been split. To avoid inadvertent data loss, please either remove the input pdf file from the source folder or the " + fileName + " subfolder from the output folder and run the script again.")
    
    os.makedirs(output_dir)
    
    
    fileName = fileName.split("_")

    #Date (we now from line 17-19, where to find year and month in the fileName list of Strings)
    year = fileName[1]
    month = fileName[2]

    # Now stitch the name of the new (split) pdf files together, with the employee names extracted from the employee.txt file 
    output_names = [year + sep + month + sep + employee for employee in employees]

    #Splitting the PDF and writing new files.

    inputPdf = PdfFileReader("source/" + input_file, "rb")

    if inputPdf.getNumPages() != len(employees):
        raise Exception("Check that number of pages in input pdf equals number of employees")

    else:
        for i in range(len(output_names)):
            output = PdfFileWriter()
            output.addPage(inputPdf.getPage(i))
            with open(output_dir + "/" + output_names[i] + ".pdf", "wb") as outputStream:
                    output.write(outputStream)
                    outputStream.close()
