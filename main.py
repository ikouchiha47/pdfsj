import sys
from os import rmdir
import time
import mimetypes
from PyPDF2 import PdfFileWriter, PdfFileReader, PdfFileMerger
from pathlib import PurePath
import progressbar as pb
from threading import Thread


def split_into_single_pages(src_pdf, out_path):
    pages = []
    count = src_pdf.numPages


    with pb.ProgressBar(max_value = count) as bar:
        for i in range(count):
            output_pdf = PdfFileWriter()
            output_pdf.addPage(src_pdf.getPage(i))
        
            out_file = "{}/doc_{}.pdf".format(out_path, i)

            with open(out_file, "wb") as f: output_pdf.write(f)
            pages.append(out_file)
            bar.update(i)

    return pages

def merge_thread(pdf_merger, ofname):
    with open(ofname, "wb") as f:
        pdf_merger.write(f)

def merge_back(pages, out_file_name):
    pdf_merger = PdfFileMerger()


    with pb.ProgressBar(max_value = len(pages)) as bar:
        for i, page in enumerate(pages):
            pdf_merger.append(page)
            bar.update(i)

    print("writing to {}. this may take some time".format(out_file_name))
    
    th = Thread(target=merge_thread, args=(pdf_merger, out_file_name))
    
    widgets = ['Processing: ', pb.AnimatedMarker(markers="-\|/-")]
    bar = pb.ProgressBar(widgets=widgets, max_value=pb.UnknownLength)
    
    th.start()
    i = 0
    while th.is_alive():
        time.sleep(0.1)
        i += 1
        bar.update(i)
    th.join()

    return out_file_name

if __name__ == "__main__":
    input_file = sys.argv[1]

    assert not (input_file == None or input_file.strip() == ""), "please provide a file name after command"


    file_type, encoding = mimetypes.guess_type(input_file)
    assert file_type == "application/pdf", "Not a valid pdf file"

    out_file_name = "out/{}".format(PurePath(input_file).name)
    src_pdf = PdfFileReader(open(input_file, "rb"))
    
    print("generating pages")
    pages = split_into_single_pages(src_pdf, "out/pages")
   
    print("merging into one")
    merge_back(pages, out_file_name)
    
    print("generated successfully")

    print("deleting generated files from out/pages")
    rmdir("out/pages/")

