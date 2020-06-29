import sys
import glob
import mimetypes
from PyPDF2 import PdfFileWriter, PdfFileReader, PdfFileMerger
from pathlib import PurePath


def split_into_single_pages(src_pdf):
    pages = []
    
    for i in range(src_pdf.numPages):
        output_pdf = PdfFileWriter()
        output_pdf.addPage(src_pdf.getPage(i))
        
        out_file = "out/doc_%s.pdf" % i
        with open(out_file, "wb") as f:
            output_pdf.write(f)
        pages.append(outFile)

    return pages


def merge_back(pages, out_file_name):
    pdf_merger = PdfFileMerger()

    for page in pages:
        pdf_merger.append(page)

    with open(out_file_name, "wb") as f:
        pdf_merger.write(f)

    return out_file_name

if __name__ == "__main__":
    input_file = sys.argv[1]

    assert (input_file == None or input_file.strip() == ""), "please provide a file name after command"


    file_type, encoding = mimetypes.guess_type(input_file)
    assert file_type == "application/pdf", "Not a valid pdf file"

    out_file_name = "out/{}".format(PurePath(input_file).name)
    src_pdf = PdfFileReader(open(input_file, "rb"))
    pages = split_into_single_pages(src_pdf)
    
    if merge_back(pages, out_file_name):
        print("{} generated success fully".format(out_file_name))
