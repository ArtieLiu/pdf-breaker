import os
import shutil

from PyPDF2 import PdfFileReader, PdfFileWriter

BOOK_NAME = "visual group theory"
BREAKS = {
    1: "cover1",
    10: "preface",
    12: "contents",
    16: "overview",
    18: "ch1",
    276: "answers",
    304: "index",
    310: "index2",
}


class Reader:
    def __init__(self, book):
        self.book = book
        self.pdf_reader = PdfFileReader(book + ".pdf")
        self.all_page_numbers = range(1, len(self.pdf_reader.pages) + 1)

    def get_page_content(self, page_number):
        return self.pdf_reader.getPage(page_number - 1)

    def is_last_page(self, page_number):
        return len(self.pdf_reader.pages) == page_number

    def next_page(self, page_number):
        return page_number + 1


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

    def dump_pages_to(self, dirname, title):
        output_file_path = os.path.join(dirname, f"{self.prefix} {title}.pdf")
        self.prefix += 1
        with open(output_file_path, 'wb') as f:
            self.pdf_writer.write(f)


def split_book(book_name, breaks: dict):
    reader = Reader(book_name)
    writer = Writer()
    make_or_empty_dir(book_name)

    for page_number in reader.all_page_numbers:
        if page_number in breaks.keys():
            cache_title = breaks[page_number]

        writer.add_page(reader.get_page_content(page_number))

        if reader.next_page(page_number) in breaks.keys() or reader.is_last_page(page_number):
            writer.dump_pages_to(book_name, cache_title)
            writer.clear()


if __name__ == '__main__':
    split_book(BOOK_NAME, BREAKS)
