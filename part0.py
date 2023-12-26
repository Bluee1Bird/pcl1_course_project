"""
PCL 1 Fall Semester 2023 - Course Project
Part 0: Book Selection
Students: <person 1>, <person 2>
"""

# --- Imports ---
import os
import re as re
import json


# --- Don't add other imports here ---


def json_conversion_sentiment(file_path: str):
    """
    Convert a text file with sentiment data to a JSON file.

    Parameters:
    - file_path (str): The path to the input text file containing sentiment data.

    Returns:
    None

    Reads the content of the specified text file, processes it to create a dictionary,
    and then converts the dictionary to a JSON object with an indentation of 4 spaces.
    The resulting JSON object is then written to a file with the same name as the input
    text file but with a '.json' extension.

    Note:
    The input text file should have lines in the format "key: value", and each pair
    should be on a new line. The function uses ':' as the delimiter to separate key and
    value pairs.
    """
    file_dict = {}
    with open(file_path, "r", encoding="UTF8") as file:
        for line in file:
            file_dict[line.split(":")[0].strip("\\\"\n ")] = line.split(":")[1]

    json_object = json.dumps(file_dict, indent=4)
    write_as_json(json_object, file_path)


def json_conversion_entity(file_path: str):
    """
    Convert a text file with entity data to a JSON file.

    Parameters:
    - file_path (str): The path to the input text file containing entity data.

    Returns:
    None

    Reads the content of the specified text file, processes it to create a dictionary
    where keys are unique entities and values are the counts of occurrences.
    The resulting dictionary is then converted to a JSON object.
    The JSON object is written to a file with the same name as the input text file but
    with a '.json' extension.

    Note:
    The input text file should contain entities on separate lines. The function counts
    the occurrences of each unique entity and creates a dictionary with entity as the key
    and count as the value.
    """

    file_dict = {}
    with open(file_path, "r", encoding="UTF8") as file:
        for line in file:
            #line.replace("")
            line = line.strip("\\\"\n ")
            if line in file_dict:
                file_dict[line] += 1
            else:
                file_dict[line] = 1

    print("file_dict:", file_dict)
    json_object = json.dumps(file_dict)
    print("json_object", json_object)
    write_as_json(json_object, file_path)


def write_as_json(data: str, file_path: str):
    """
    Write data to a JSON file.

    Parameters:
    - data: The data to be written to the JSON file.
    - file_path (str): The path to the output JSON file.

    Returns:
    None

    Takes the provided data and writes it to a JSON file with the specified file path.

    Note:
    The function automatically appends '.json' to the original file name for the output
    JSON file. If the input file path is "example.txt", the output JSON file will be
    named "example.json".
    """
    json_file_path = file_path.split(".")[0] + ".json"
    with open(json_file_path, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file)




def splitSentimentIntoChapters(book: str, file_path: str):
    """
    Split sentiment data into separate files for each chapter.

    Parameters:
    - book (str): The name of the book or project directory.
    - file_path (str): The path to the input file containing sentiment data for all chapters.

    Returns:
    None

    Reads the content of the specified file containing sentiment data for all chapters.
    Creates individual text files for each chapter within the specified book directory.
    Writes the corresponding sentiment data to the respective chapter files.

    Note:
    The input file should have lines in the format "chapter_number.sentiment_data".
    The function reads the chapter number from the line and creates separate text files
    for each chapter in the specified book directory.
    The sentiment data for each chapter is then written to the corresponding chapter file
    in the format "word: sentiment_value".
    """

    with open(file_path, "r", encoding="UTF8") as allChapters:
    # make all the files you will need (one for each chapter)
        second_word = False
        allChapters.readline()  # read the first line here already, because the first will be a text line
        while not second_word:
            line = allChapters.readline()
            if line[0].isdigit():
                open(book + "/" + str(line[0]) + "_Sentiment.txt", "w", encoding="UTF8")  # make the file
            else:
                second_word = True
    # write to the files you've just created.
    with open(file_path, "r", encoding="UTF8") as allChapters:

        current_word = ""
        for line in allChapters:
            if line[0].isalpha():
                current_word = line
            elif line[0].isdigit():
                with open(book + "/" + line.split('.')[0] + "_Sentiment.txt", "a", encoding="UTF8") as file:
                    file.write(current_word.strip() + ":" + line.split(':')[1])


def splitEntitiesIntoChaptes(file_path: str, book: str):
    """
    Split entity data into separate files for each chapter.

    Parameters:
    - file_path (str): The path to the input file containing entity data for all chapters.
    - book (str): The name of the book or project directory.

    Returns:
    None

    Reads the content of the specified file containing entity data for all chapters.
    Creates individual text files for each chapter within the specified book directory.
    Writes the corresponding entity data to the respective chapter files.

    Note:
    The input file should have lines in the format "chapter_number: entity_data".
    The function reads the chapter number from the line and creates separate text files
    for each chapter in the specified book directory.
    The entity data for each chapter is then written to the corresponding chapter file.
    """

    with open(file_path, "r", encoding="UTF8") as allChapters:

        current_chapter = ""
        for line in allChapters:
            if line[0] != current_chapter: # make the file
                open(book + "/" + str(line[0]) + "_Entities.txt", "w", encoding="UTF8")  # make the file
                current_chapter = line[0]
            # write to the file
            with open(book + "/" + str(current_chapter) + "_Entities.txt", "a", encoding="UTF8") as file:
                write = line.split(':')[1].strip()+"\n"
                file.write(write)


def iterateThroughFiles(book: str):
    """
    Iterate through files in a specified directory and perform conversions.

    Parameters:
    - book (str): The name of the directory containing the files to be processed.

    Returns:
    None

    Iterates through files in the specified directory and performs conversions based on
    file type. If a file contains "Sentiment" in its name, it calls the
    `json_conversion_sentiment` function. If it contains "Entities", it calls the
    `json_conversion_entity` function.

    Note:
    The function assumes that the input directory (specified by the 'book' parameter)
    contains files related to sentiment and entity data. It uses file names to determine
    which conversion function to apply.
    """

    path = r"C:\Users\maaik\PycharmProjects\pcl1_course_project" + "\\" + book

    for filename in os.listdir(path):
        file_path = os.path.join(path, filename)
        if file_path.__contains__("Sentiment"):
            json_conversion_sentiment(file_path)
        elif file_path.__contains__("Entities"):
            json_conversion_entity(file_path)


def main():
    """
    Perform sentiment and entity data processing for specified books.

    Returns:
    None

    Executes a sequence of functions to process sentiment and entity data for three
    books: "the_great_gatsby," "pride_and_prejudice," and "little_women."

    1. Calls `splitSentimentIntoChapters` for each book and its corresponding sentiment file.
    2. Calls `splitEntitiesIntoChapters` for each book and its corresponding entities file.
    3. Calls `iterateThroughFiles` for each book to convert the processed data to JSON format.

    Note:
    Ensure that the directory structure and file paths match the specified books and files.
    The function assumes the existence of sentiment and entities files for each book in the
    specified directories.
    """

    splitSentimentIntoChapters("the_great_gatsby", "./the_great_gatsby/sentiment.txt")
    splitSentimentIntoChapters("pride_and_prejudice", "./pride_and_prejudice/sentiment.txt")
    splitSentimentIntoChapters("little_women", "./little_women/sentiment.txt")

    splitEntitiesIntoChaptes("./the_great_gatsby/entities.txt", "the_great_gatsby")
    splitEntitiesIntoChaptes("./pride_and_prejudice/entities.txt", "pride_and_prejudice")
    splitEntitiesIntoChaptes("./little_women/entities.txt", "little_women")

    iterateThroughFiles("little_women")
    iterateThroughFiles("pride_and_prejudice")
    iterateThroughFiles("the_great_gatsby")


# This is the standard boilerplate that calls the main() function when the program is executed.
if __name__ == '__main__':
    main()
