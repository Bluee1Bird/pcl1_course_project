##############################################################################################################
##############################################################################################################
##### DO NOT MODIFY THIS CODE #####
# This code is to be used as is.

import os
import re
import sys
import argparse

# Markers for the start and end of Project Gutenberg headers/footers
TEXT_START_MARKERS = frozenset((
    "*END*THE SMALL PRINT",
    "*** START OF THE PROJECT GUTENBERG",
    "*** START OF THIS PROJECT GUTENBERG",
    "This etext was prepared by",
    "E-text prepared by",
    "Produced by",
    "Distributed Proofreading Team",
    "Proofreading Team at http://www.pgdp.net",
    "http://gallica.bnf.fr)",
    "      http://archive.org/details/",
    "http://www.pgdp.net",
    "by The Internet Archive)",
    "by The Internet Archive/Canadian Libraries",
    "by The Internet Archive/American Libraries",
    "public domain material from the Internet Archive",
    "Internet Archive)",
    "Internet Archive/Canadian Libraries",
    "Internet Archive/American Libraries",
    "material from the Google Print project",
    "*END THE SMALL PRINT",
    "***START OF THE PROJECT GUTENBERG",
    "This etext was produced by",
    "*** START OF THE COPYRIGHTED",
    "The Project Gutenberg",
    "http://gutenberg.spiegel.de/ erreichbar.",
    "Project Runeberg publishes",
    "Beginning of this Project Gutenberg",
    "Project Gutenberg Online Distributed",
    "Gutenberg Online Distributed",
    "the Project Gutenberg Online Distributed",
    "Project Gutenberg TEI",
    "This eBook was prepared by",
    "http://gutenberg2000.de erreichbar.",
    "This Etext was prepared by",
    "This Project Gutenberg Etext was prepared by",
    "Gutenberg Distributed Proofreaders",
    "Project Gutenberg Distributed Proofreaders",
    "the Project Gutenberg Online Distributed Proofreading Team",
    "**The Project Gutenberg",
    "*SMALL PRINT!",
    "More information about this book is at the top of this file.",
    "tells you about restrictions in how the file may be used.",
    "l'authorization à les utilizer pour preparer ce texte.",
    "of the etext through OCR.",
    "*****These eBooks Were Prepared By Thousands of Volunteers!*****",
    "We need your donations more than ever!",
    " *** START OF THIS PROJECT GUTENBERG",
    "****     SMALL PRINT!",
    '["Small Print" V.',
    '      (http://www.ibiblio.org/gutenberg/',
    'and the Project Gutenberg Online Distributed Proofreading Team',
    'Mary Meehan, and the Project Gutenberg Online Distributed Proofreading',
    '                this Project Gutenberg edition.',
))

TEXT_END_MARKERS = frozenset((
    "*** END OF THE PROJECT GUTENBERG",
    "*** END OF THIS PROJECT GUTENBERG",
    "***END OF THE PROJECT GUTENBERG",
    "End of the Project Gutenberg",
    "End of The Project Gutenberg",
    "Ende dieses Project Gutenberg",
    "by Project Gutenberg",
    "End of Project Gutenberg",
    "End of this Project Gutenberg",
    "Ende dieses Projekt Gutenberg",
    "        ***END OF THE PROJECT GUTENBERG",
    "*** END OF THE COPYRIGHTED",
    "End of this is COPYRIGHTED",
    "Ende dieses Etextes ",
    "Ende dieses Project Gutenber",
    "Ende diese Project Gutenberg",
    "**This is a COPYRIGHTED Project Gutenberg Etext, Details Above**",
    "Fin de Project Gutenberg",
    "The Project Gutenberg Etext of ",
    "Ce document fut presente en lecture",
    "Ce document fut présenté en lecture",
    "More information about this book is at the top of this file.",
    "We need your donations more than ever!",
    "END OF PROJECT GUTENBERG",
    " End of the Project Gutenberg",
    " *** END OF THIS PROJECT GUTENBERG",
))

LEGALESE_START_MARKERS = frozenset(("<<THIS ELECTRONIC VERSION OF",))

LEGALESE_END_MARKERS = frozenset(("SERVICE THAT CHARGES FOR DOWNLOAD",))


def strip_headers(text: str) -> str:
    """Remove lines that are part of the Project Gutenberg header or footer."""
    lines = text.splitlines()
    sep = str(os.linesep)

    out = []
    i = 0
    footer_found = False
    ignore_section = False

    for line in lines:
        reset = False

        # Header removal
        if i <= 600 and any(line.startswith(token) for token in TEXT_START_MARKERS):
            reset = True

        if reset:
            out = []
            continue

        # Footer detection
        if i >= 100 and any(line.startswith(token) for token in TEXT_END_MARKERS):
            footer_found = True

        if footer_found:
            break

        # Legalese removal
        if any(line.startswith(token) for token in LEGALESE_START_MARKERS):
            ignore_section = True
            continue
        elif any(line.startswith(token) for token in LEGALESE_END_MARKERS):
            ignore_section = False
            continue

        if not ignore_section:
            out.append(line.rstrip(sep))
            i += 1

    return sep.join(out)


##############################################################################################################
##############################################################################################################

#### MODIFY HERE ####

def split_book_by_chapter(cleaned_text: str, book_title:str):
    """
    Split the provided cleaned text into chapters and save each chapter in a separate file.

    Parameters:
    - cleaned_text (str): The cleaned text of the book to be split into chapters.
    - book_title (str): The title of the book, used to create a folder for saving the chapters.

    Returns:
    None

    The function creates a folder named after the book title and saves the entire cleaned text
    in a file named 'book_title_clean.txt' within that folder. Additionally, it splits the text
    into chapters using the string "CHAPTER" as a delimiter and saves each chapter in a separate
    file under a subfolder named 'chapters'. The files are named numerically (e.g., '0.txt', '1.txt', etc.).
    """

    # 3. Save the cleaned text in the book title folder

    folder_path = book_title

    # Check if the folder exists, if not, create it
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    # Specify the file path within the folder
    file_path = os.path.join(folder_path, book_title + "_clean.txt")

    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(cleaned_text)

    # 4. Split the text into chapters and save them in the book title folder under a subfolder named 'chapters'

    chapters = re.split("\n\s*CHAPTER\s", cleaned_text)
    print(chapters)

    chapter_path = os.path.join(folder_path, "chapters")

    # Check if the folder exists, if not, create it
    if not os.path.exists(chapter_path):
        os.makedirs(chapter_path)

    for number, chapter in enumerate(chapters):
        file_path = os.path.join(chapter_path, str(number) + ".txt")

        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(chapter)


def main():
    """
    Parse the command line arguments, read a text file, clean the text, and split it into chapters.

    Usage:
    python script_name.py <path_to_book_file>

    Parameters:
    None

    The function uses argparse to handle command line arguments, expecting the relative path
    of the book file to be provided. It then reads the text from the file, cleans it using the
    strip_headers function, and splits it into chapters using the split_book_by_chapter function.
    The book title is extracted from the file path and used for creating a folder to save the chapters.
    """
    # Initialize parser
    parser = argparse.ArgumentParser(description="add relative path of the book you want to parse")
    parser.add_argument("file_path")

    args = parser.parse_args()
    if len(sys.argv) != 2:
        print("Usage: python gutenberg_cleanup.py <path_to_book_file>")
        # sys.exit(1)

    file_path = args.file_path
    book_title = os.path.basename(file_path).replace('.txt', '')

    print(book_title)

    # 1. Read the text file

    with open(file_path, "r", encoding="UTF8") as book:
        text = book.read()

    # 2. Clean the text

    cleaned_text = strip_headers(text)

    split_book_by_chapter(cleaned_text, book_title)


if __name__ == '__main__':
    main()
