import os
import shutil

from PyPDF2 import PdfFileReader, PdfFileWriter

book_name = "visual group theory"
breaks = {
    1: "cover1",
    10: "preface",
    12: "contents",
    16: "overview",
    18: "ch1",
    276: "answers",
    304: "index",
    312: "about",
}
PREFIX = 0


class Reader:
    def __init__(self, book):
        self.book = book
        self.pdf_reader = PdfFileReader(book + ".pdf")
        self.all_pages = range(1, len(self.pdf_reader.pages) + 1)

    def get_page(self, page_number):
        return self.pdf_reader.getPage(page_number - 1)


def make_or_empty_dir(folder):
    if os.path.isdir(folder):
        shutil.rmtree(folder)
    os.mkdir(folder)


class Writer:
    def __init__(self):
        self.pdf_writer = PdfFileWriter()
        self.prefix = 0

    def add_page(self, page):
        self.pdf_writer.addPage(page)

    def clear(self):
        self.pdf_writer = PdfFileWriter()

    def dump_pages_to(self, folder, title):
        output_file_path = os.path.join(book_name, f"{self.prefix} {title}.pdf")
        self.prefix += 1
        with open(output_file_path, 'wb') as f:
            self.pdf_writer.write(f)


def split_book(book_name, breaks: dict):
    reader = Reader(book_name)
    writer = Writer()
    make_or_empty_dir(book_name)

    for page_number in reader.all_pages:
        if page_number in breaks.keys():
            cache_title = breaks[page_number]

        writer.add_page(reader.get_page(page_number))

        if page_number + 1 in breaks.keys():
            writer.dump_pages_to(book_name, cache_title)
            writer.clear()


if __name__ == '__main__':
    split_book(book_name, breaks)
