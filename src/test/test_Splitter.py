import os.path
import shutil
from unittest import TestCase

from pypdf import PdfReader

from src.main.Splitter import split_pdf

dirname = os.path.dirname(__file__)
PDF_FILE = os.path.join(dirname, './test_data/refactoring.pdf')
OUTPUT_DIR = os.path.join(dirname, './test_data/refactoring')


class Test(TestCase):

    def tearDown(self):
        if os.path.isdir(OUTPUT_DIR):
            shutil.rmtree(OUTPUT_DIR)

    def test_split_pdf(self):
        breaks = {
            1: "cover",
            8: "contents",
            442: "index",
        }

        split_pdf(breaks=breaks,
                  filepath=PDF_FILE,
                  output_path=OUTPUT_DIR)

        cover_name = "1   7    cover.pdf"
        contents_name = "2   434  contents.pdf"
        index_name = "3   20   index.pdf"

        self.assert_has_pages(f"{OUTPUT_DIR}/{cover_name}", 7)
        self.assert_has_pages(f"{OUTPUT_DIR}/{contents_name}", 434)
        self.assert_has_pages(f"{OUTPUT_DIR}/{index_name}", 20)

    def assert_has_pages(self, pdf_path, expected_total_pages):
        self.assertEqual(len(PdfReader(pdf_path).pages), expected_total_pages)
