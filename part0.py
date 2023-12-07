"""
PCL 1 Fall Semester 2023 - Course Project
Part 0: Book Selection
Students: <person 1>, <person 2>
"""

# --- Imports ---
import os
import re
import json


# --- Don't add other imports here ---


def json_conversion_sentiment(file_path):
    file_dict = {}
    with open(file_path, "r", encoding="UTF8") as file:
        for line in file:
            file_dict[line.split(":")[0]] = line.split(":")[1]

    json_object = json.dumps(file_dict, indent=4)
    write_as_json(json_object, file_path)


def json_conversion_entity(file_path):
    file_dict = {}
    with open(file_path, "r", encoding="UTF8") as file:
        for line in file:
            if line in file_dict:
                file_dict[line] += 1
            else:
                file_dict[line] = 1

    json_object = json.dumps(file_dict, indent=4)
    write_as_json(json_object, file_path)


def write_as_json(data, file_path):
    """
    Create a function to write your json string to a file here.
    Think about a naming convention for the output files.
    """
    json_file_path = file_path.split(".")[0] + ".json"
    with open(json_file_path, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)




def splitSentimentIntoChapters(book, file_path):

    with open(file_path, "r", encoding="UTF8") as allChapters:
    # make all the files you will need (one for each chapter)
        second_word = False
        allChapters.readline()  # read the first line here already, because the first will be a text line
        while not second_word:
            line = allChapters.readline()
            print(line)
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


def splitEntitiesIntoChaptes(file_path, book):
    with open(file_path, "r", encoding="UTF8") as allChapters:

        current_chapter = ""
        for line in allChapters:
            if line[0] != current_chapter: # make the file
                open(book + "/" + str(line[0]) + "_Entities.txt", "w", encoding="UTF8")  # make the file
                current_chapter = line[0]
            # write to the file
            with open(book + "/" + str(current_chapter) + "_Entities.txt", "a", encoding="UTF8") as file:
                file.write(line.split(':')[1])


def main():
    # splitSentimentIntoChapters("the_great_gatsby", "./the_great_gatsby/sentiment.txt", "Sentiment")
    # splitSentimentIntoChapters("pride_and_prejudice", "./pride_and_prejudice/sentiment.txt", "Sentiment")
    # splitSentimentIntoChapters("little_women", "./little_women/sentiment.txt", "Sentiment")

    # splitEntitiesIntoChaptes("./the_great_gatsby/entities.txt", "the_great_gatsby")
    # splitEntitiesIntoChaptes("./pride_and_prejudice/entities.txt", "pride_and_prejudice")
    # splitEntitiesIntoChaptes("./little_women/entities.txt", "little_women")

    iterateThroughFiles("little_women")
    iterateThroughFiles("pride_and_prejudice")
    iterateThroughFiles("the_great_gatsby")


def iterateThroughFiles(book):
    path = r"C:\Users\maaik\PycharmProjects\pcl1_course_project" + "\\" + book

    for filename in os.listdir(path):
        file_path = os.path.join(path, filename)
        if file_path.__contains__("Sentiment"):
            print("sentiment")
            json_conversion_sentiment(file_path)
        elif file_path.__contains__("Entities"):
            print("enitity")
            json_conversion_entity(file_path)


# This is the standard boilerplate that calls the main() function when the program is executed.
if __name__ == '__main__':
    main()
