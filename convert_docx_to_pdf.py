from pathlib import Path
import comtypes.client
from glob import glob

wd_format_pdf = 17

input_files = glob(".\doc\*.docx")

word = comtypes.client.CreateObject("Word.Application")

for file in input_files:
    in_file = str(Path(file).absolute())
    out_file = str(Path(file).absolute()).replace("docx","pdf")
    doc = word.Documents.Open(in_file)
    doc.SaveAs(out_file, FileFormat=wd_format_pdf)
    doc.Close()
    # print(out_file)

word.Quit()