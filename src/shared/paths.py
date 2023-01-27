import os
from pathlib import Path


this_file = Path(os.path.dirname(__file__))
repo_folder: Path = this_file.parent.parent
output_folder = repo_folder / "output"

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

nusmvfilename = "nusmvfile.smv"
nusmv_file_path = output_folder / nusmvfilename
