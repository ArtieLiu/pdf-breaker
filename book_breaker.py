import os
import shutil

from Reader import Reader
from Writer import Writer

BOOK_NAME = "design patterns"

rough_breaks = {
    1: "front",
    7: "cover",
    11: "contents",
    15: "preface",
    17: "forward",
    21: "chapters",
}

chapter_breaks = {
    "1 case study": 1,
    "2 design pattern catalog": 79,
    "3 appendix": 359,
    "4 index": 383
}


def make_or_empty_dir(folder):
    if os.path.isdir(folder):
        shutil.rmtree(folder)
    os.mkdir(folder)


def split_pdf(pdf_name, breaks: dict):
    def is_end_of_section():
        return reader.next_page_number() in breaks.keys()

    def is_end_of_book():
        return reader.is_last_page()

    reader = Reader(filepath=f"./{pdf_name}.pdf")
    writer = Writer(write_to=pdf_name)

    for page_number in reader.page_numbers:
        if page_number in breaks.keys():
            section_name = breaks[page_number]

        writer.add_page(reader.get_page_content(page_number))

        if is_end_of_section() or is_end_of_book():
            writer.dump_pages_to(section_name)
            writer.clear()

        reader.turn_page()


def rough_split(BOOK_NAME, rough_breaks):
    split_pdf(BOOK_NAME, rough_breaks)


def split_chapters(filename, chapter_breaks):
    split_pdf(BOOK_NAME, chapter_breaks)


if __name__ == '__main__':
    make_or_empty_dir(BOOK_NAME)

    rough_split(BOOK_NAME, rough_breaks)
    # split_chapters("6 397 chapters.pdf", chapter_breaks)
    # remove_file("chapters.pdf")
