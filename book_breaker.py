import os
import shutil

from pypdf import PdfReader, PdfWriter

BOOK_NAME = "refactoring"
BREAKS = {
    1: "front",
    4: "cover",
    8: "contents",
    14: "forward",
    16: "preface",
    24: "ch1-8",
    260: "ch9-15",
    436: "ref",
    442: "index",
    458: "other"
}

book = {
    "book": "refactoring.pdf",
    "sections": {
        "front": 1,
        "cover": 3,
        "toc": 10,
        "chapters": 15,
        "rear": 160
    }
}

chapters = {
    "ch1": 1,
    "ch2": 20
}


class Reader:
    def __init__(self, book):
        self.book = book
        self.pdf_reader = PdfReader(book + ".pdf")
        self.all_page_numbers = range(1, len(self.pdf_reader.pages) + 1)

    def get_page_content(self, page_number):
        return self.pdf_reader.pages[page_number - 1]

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
        self.pdf_writer = PdfWriter()
        self.batch_num = 1

    def add_page(self, page):
        self.pdf_writer.add_page(page)

    def clear(self):
        self.pdf_writer = PdfWriter()

    def total_pages(self):
        return len(self.pdf_writer.pages)

    def dump_pages_to(self, dirname, title):
        batch_number = str(self.batch_num).ljust(3)
        total_pages = str(self.total_pages()).ljust(4)
        filename = f"{batch_number} {total_pages} {title}.pdf"

        output_file_path = os.path.join(dirname, filename)

        with open(output_file_path, 'wb') as f:
            self.pdf_writer.write(f)

        self.batch_num += 1


def split_book(book_name, breaks: dict):
    reader = Reader(book_name)
    writer = Writer()
    make_or_empty_dir(book_name)

    for page_number in reader.all_page_numbers:
        print(f"doing {page_number}")
        if page_number in breaks.keys():
            cache_title = breaks[page_number]

        writer.add_page(reader.get_page_content(page_number))

        if reader.next_page(page_number) in breaks.keys() or reader.is_last_page(page_number):
            writer.dump_pages_to(book_name, cache_title)
            writer.clear()


if __name__ == '__main__':
    split_book(BOOK_NAME, BREAKS)
