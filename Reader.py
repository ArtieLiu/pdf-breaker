from pypdf import PdfReader


class Reader:
    current_page: int

    def __init__(self, book):
        self.book = book
        self.pdf_reader = PdfReader(book + ".pdf")
        self.current_page = 1
        self.page_numbers = range(1, len(self.pdf_reader.pages) + 1)

    def get_page_content(self, page_number):
        return self.pdf_reader.pages[page_number - 1]

    def next_page_number(self):
        return self.current_page + 1

    def turn_page(self):
        self.current_page += 1

    def is_last_page(self):
        return self.current_page == len(self.pdf_reader.pages)
