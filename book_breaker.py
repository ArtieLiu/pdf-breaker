import os
from pathlib import Path
import shutil

from Reader import Reader
from Writer import Writer


def make_or_empty_dir(folder):
    if os.path.isdir(folder):
        shutil.rmtree(folder)
    os.mkdir(folder)


def filename_of(filepath):
    return Path(filepath).stem


def split_pdf(breaks: dict, filepath):
    def is_end_of_section():
        return reader.next_page_number() in breaks.keys()

    def is_end_of_book():
        return reader.is_last_page()

    reader = Reader(filepath=filepath)
    writer = Writer(write_to=filename_of(filepath))

    for page_number in reader.page_numbers:
        if page_number in breaks.keys():
            section_name = breaks[page_number]

        writer.add_page(reader.get_page_content(page_number))

        if is_end_of_section() or is_end_of_book():
            writer.dump_pages_to(section_name)
            writer.clear()

        reader.turn_page()


if __name__ == '__main__':
    book = "design patterns.pdf"

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

    make_or_empty_dir(filename_of(book))

    split_pdf(rough_breaks, filepath=book)
