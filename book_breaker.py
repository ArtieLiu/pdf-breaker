import os
from PyPDF2 import PdfFileReader, PdfFileWriter

PREFIX = 0


def write(name, cache_writer):
    global PREFIX
    output_file_path = os.path.join("output", f"{PREFIX} {name}.pdf")
    PREFIX += 1
    with open(output_file_path, 'wb') as f:
        cache_writer.write(f)


def minus_one(number):
    return number - 1


def split_book(book_name, breaks: dict):
    reader = PdfFileReader(book_name)
    cache_writer = PdfFileWriter()
    cache_title = ""

    for page_number in range(1, len(reader.pages) + 1):
        if page_number in breaks.keys():
            cache_title = breaks[page_number]

        page = reader.getPage(minus_one(page_number))
        cache_writer.addPage(page)

        if page_number+1 in breaks.keys():
            write(cache_title, cache_writer)
            cache_writer = PdfFileWriter()


if __name__ == '__main__':
    book = "visual group theory.pdf"
    break_points = {
        1: "cover1",
        10: "preface",
        12: "contents",
        16: "overview",
        18: "ch1",
        276: "answers",
        304: "index"
    }

    split_book(book, break_points)
