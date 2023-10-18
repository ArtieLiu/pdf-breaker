import os
from PyPDF2 import PdfFileReader, PdfFileWriter

book_name = "visual group theory"
break_points = {
    1: "cover1",
    10: "preface",
    12: "contents",
    16: "overview",
    18: "ch1",
    276: "answers",
    304: "index"
}
PREFIX = 0


def write(name, cache_writer, ):
    def make_book_dir_if_not_exist():
        if os.path.isdir(book_name):
            return
        else:
            os.mkdir(book_name)

    make_book_dir_if_not_exist()
    global PREFIX
    output_file_path = os.path.join(book_name, f"{PREFIX} {name}.pdf")
    PREFIX += 1
    with open(output_file_path, 'wb') as f:
        cache_writer.write(f)


def split_book(book_name, breaks: dict):
    def read_pdf():
        book_pdf = book_name + '.pdf'
        return PdfFileReader(book_pdf)

    def get_page(page_number):
        return reader.getPage(page_number - 1)

    reader = read_pdf()
    cache_writer = PdfFileWriter()
    cache_title = ""

    for page_number in range(1, len(reader.pages) + 1):
        if page_number in breaks.keys():
            cache_title = breaks[page_number]

        page = get_page(page_number)
        cache_writer.addPage(page)

        if page_number + 1 in breaks.keys():
            write(cache_title, cache_writer)
            cache_writer = PdfFileWriter()


if __name__ == '__main__':
    split_book(book_name, break_points)
