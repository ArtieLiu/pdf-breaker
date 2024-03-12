from os import mkdir
from pathlib import Path

from Reader import Reader
from Writer import Writer


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
