import requests
import argparse

PROGRAM = "AUT Presentation Downloader"
DESCRIPTION = """ 
Given a presentation link, it downloads all of the slides.
"""

parser = argparse.ArgumentParser(prog=PROGRAM, description=DESCRIPTION)

parser.add_argument("-u", "--url", required=True, dest="url", nargs=1, help="presentation url")
parser.add_argument("-d", "--directory", dest="directory", default=".", nargs=1, help="local directory")

args = parser.parse_args()

url, = args.url
directory, = args.directory

slide_no = 1

while True:
    print(f"Requesting slide {slide_no}", end=" ")
    response = requests.get(url + f"/{slide_no}")
    print("DONE")
    if response.status_code == 200:
        with open(f"{directory}/{slide_no}.svg", "wb") as f:
            f.write(response.content)
        slide_no += 1
    else:
        print("Reached the end of presentation")
        break
