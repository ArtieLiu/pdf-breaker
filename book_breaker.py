from os import mkdir
from pathlib import Path

from Reader import Reader
from Writer import Writer


def filename_of(filepath):
    return Path(filepath).stem


def split_pdf(breaks: dict, filepath, output_path):
    def is_end_of_section():
        return reader.next_page_number() in breaks.keys()

    def is_end_of_book():
        return reader.is_last_page()

    mkdir(output_path)

    reader = Reader(filepath=filepath)
    writer = Writer(write_to=output_path)

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
    split_pdf(breaks=rough_breaks,
              filepath=book,
              output_path=filename_of(book))

    chapter_breaks = {
        1: "case study",
        79: "design pattern catalog",
        359: "appendix",
        383: "index"
    }
    split_pdf(breaks=chapter_breaks,
              filepath='./design patterns/6   397  chapters.pdf',
              output_path=f"{filename_of(book)}/chapters")
