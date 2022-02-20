import cairosvg
import requests
import argparse
import tempfile
import img2pdf
import shutil

PROGRAM = "AUT Presentation Downloader"
DESCRIPTION = """ 
Given a presentation link, it downloads all of the slides and creates a PDF file.
"""

parser = argparse.ArgumentParser(prog=PROGRAM, description=DESCRIPTION)

parser.add_argument("-u", "--url", required=True, nargs=1, help="presentation url")
parser.add_argument("-o", "--output", required=True, nargs=1, help="path to output")
parser.add_argument("-s", "--start", default=1, type=int, nargs=1, help="start downloading slides from")
parser.add_argument("-e", "--end", default=200, type=int, nargs=1, help="finish downloading slides when")

args = parser.parse_args()

url, = args.url
output, = args.output
start, = args.start
end, = args.end

slide_no = start

temp = tempfile.mkdtemp()

print("Saving temporary files to", temp)

slides = []

# TODO: Use "\x1b[1K\r" as the end argument for print
while slide_no <= end:
    print(f"Downloading slide {slide_no}", end=" ", flush=True)
    response = requests.get(url + f"/svg/{slide_no}")
    print("DONE")
    if response.status_code == 200:
        path = f"{temp}/{slide_no}.png"
        print("Converting to PNG", end=" ", flush=True)
        cairosvg.svg2png(bytestring=response.content, write_to=path)
        print("DONE")
        slide_no += 1
        slides.append(path)
    else:
        print("Reached the end of presentation")
        break

if slides:
    print("Creating PDF", end=" ", flush=True)
    with open(output, "wb") as f:
        f.write(img2pdf.convert(slides))
    print("DONE")

print(f"Removing directory {temp}", end=" ", flush=True)
shutil.rmtree(temp)
print("DONE")