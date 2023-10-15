import os
from pathlib import Path

from llama_index import download_loader

PDF_DATA_DIR = "./pdf_data/"

class PDFReader:
    def __init__(self):
        self.pdf_reader = download_loader("PDFReader", custom_path="local_dir")()

    def load_data(self, file_name):
        return self.pdf_reader.load_data(file=Path(PDF_DATA_DIR + file_name))