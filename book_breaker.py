import os
from PyPDF2 import PdfFileReader, PdfFileWriter


def break_pages_by(break_points):
    return {
        "cover1": [1, 2],
        "preface": [3, 4, 5]
    }


def write_to_file(name, page_numbers):
    writer = PdfFileWriter()
    reader = PdfFileReader(book)
    for page_number in page_numbers:
        page = reader.getPage(page_number - 1)
        writer.addPage(page)

    output_file_path = os.path.join("output", f"{name}.pdf")
    with open(output_file_path, 'wb') as f:
        writer.write(f)


if __name__ == '__main__':
    book = "visual group theory.pdf"
    break_points = {
        1: "cover1",
        2: "cover2",
        10: "preface",
        12: "contents",
        16: "overview",
        18: "ch1",
        276: "answers",
        304: "index"
    }

    pages_of_parts = break_pages_by(break_points)

    for part_name, numbers in pages_of_parts.items():

        write_to_file(part_name, numbers)
