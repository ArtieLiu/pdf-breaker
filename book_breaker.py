import os
import shutil

from pypdf import PdfReader, PdfWriter

BOOK_NAME = "refactoring"

rough_breaks = {
    "front": 1,
    "cover": 4,
    "contents": 8,
    "forward": 14,
    "preface": 16,
    "chapters": 24,
}

chapter_breaks = {
    "ch1": 1,
    "ch8": 169,
    "refs": 413,
    "index": 419
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


def split_pdf(book_name, breaks: dict):
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


def rough_split(BOOK_NAME, rough_breaks):
    split_pdf(BOOK_NAME, rough_breaks)


def split_chapters(filename, chapter_breaks):
    split_pdf(BOOK_NAME, chapter_breaks)


def remove_file(filename):
    pass


if __name__ == '__main__':
    # split_book(BOOK_NAME, BREAKS)
    rough_split(BOOK_NAME, rough_breaks)
    split_chapters("chapters.pdf", chapter_breaks)
    remove_file("chapters.pdf")
