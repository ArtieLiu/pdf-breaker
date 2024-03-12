from Splitter import split_pdf
from utils import filename_of

if __name__ == '__main__':
    book = "refactoring.pdf"
    rough_breaks = {
        1: "front",
        4: "cover",
        8: "contents",
        14: "forward",
        24: "chapters",
        436: "ref",
        442: "index",
        455: "list of refactorings",
        458: "others"
    }
    split_pdf(breaks=rough_breaks,
              filepath=book,
              output_path=filename_of(book))

    chapter_breaks = {
        1: "ch1-8",
        237: "ch9-15",
    }
    split_pdf(breaks=chapter_breaks,
              filepath='./refactoring/5   412  chapters.pdf',
              output_path=f"{filename_of(book)}/chapters")
