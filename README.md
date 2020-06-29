# pdfsj

As I was reading a pdf, the pdf file was a double paged pdf. That made reading hard.

This tool attempts to split a multi paged pdf and concatenate into a single paged pdf.

### Requirements
- python 3.8+
- virtualenv

### Running
- python main.py /path/to/painful/pdf

The resulting file can be found in `./out/`


TODO:
- pdf merging is slow, will switch to something like ghostscript
