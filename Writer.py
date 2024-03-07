import os

from pypdf import PdfWriter


class Writer:
    def __init__(self, write_to):
        self.pdf_writer = PdfWriter()
        self.write_to = write_to
        self.batch_num = 1

    def add_page(self, page):
        self.pdf_writer.add_page(page)

    def clear(self):
        self.pdf_writer = PdfWriter()

    def get_total_num_of_pages(self):
        return len(self.pdf_writer.pages)

    def dump_pages_to(self, title):
        batch_number = format(self.batch_num, width=3)
        total_pages = format(self.get_total_num_of_pages(), width=4)
        filename = f"{batch_number} {total_pages} {title}.pdf"

        output_file_path = os.path.join(self.write_to, filename)

        with open(output_file_path, 'wb') as f:
            self.pdf_writer.write(f)

        self.batch_num += 1


def format(num, width):
    return str(num).ljust(width)
