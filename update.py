import os
import glob
import shutil
import zipfile
import requests

print("Fetching Updates...")
r = requests.get('https://github.com/smrflynn/Seating_Chart/archive/master.zip')

with open("tmp.zip", "wb") as f:
    f.write(r.content)

print("Fetching Updates... COMPLETE")
print("Updating Files...")
with zipfile.ZipFile("tmp.zip", "r") as zip_ref:
    zip_ref.extractall()

src_folder = "Seating_Chart-master"
dst_folder = os.getcwd()

# remove old file from destination
for file in glob.glob(dst_folder + "\\*"):
    if "update" in file:
        pass
    elif os.path.isfile(file):
        os.remove(file)

for file in glob.glob(src_folder + "\\*"):
    if "update" in file:
        pass
    if os.path.isfile(file):
        shutil.move(file, dst_folder)

os.rmdir("Seating_Chart-master")
print("Updating Files... COMPLETE")

