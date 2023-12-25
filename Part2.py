"""
PCL 1 Fall Semester 2023 - Course Project
Part 0: Book Selection
Students: <person 1>, <person 2>
"""
# --- Imports ---
from statistics import mean
import json
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


# Function to perform sentiment analysis
def analyze_sentiment(character_dicts, analyzer):
    """
    Analyzes sentiment for a list of character occurrences in a book.

    Args:
    - character_dicts (list of dict): A list of dictionaries, each representing a character's occurrences
        in the book. Each dictionary should contain an 'occurrences' key with a list of sentences where
        the character appears.
    - analyzer: An object with a 'polarity_scores' method that computes sentiment scores for sentences.

    Returns:
    None

    This function analyzes the sentiment of sentences associated with each character's occurrences in the book.
    It calculates the sentiment scores for each sentence and stores them in the 'sentiment' key of each occurrence.
    It also computes and stores the average sentiment scores per chapter and for the entire book for each character.

    After calling the function, each character dictionary will have sentiment scores and averages.
    """

    # Iterate over each character and access the 'sentence' property to analyze it
    for character in character_dicts:

        # define data structures to be able to calculate averages over the chapters and the entire book
        compound_entire_book = []
        compound_per_chapter = {}

        # access every occurrence of a character in the book for the sentiment analysis
        for occurrence in character['occurrences']:
            sentence = occurrence["sentence"]

            # calculate the sentiment score and add it to the dictionary with a new key
            sentiments = analyzer.polarity_scores(sentence)
            occurrence["sentiment"] = sentiments

            compound = sentiments["compound"]
            compound_entire_book.append(compound)

            # add the value to the compound per chapter dict
            # there is a key for every chapter, add to that if there already exists a value for the chapter
            # if not, add a new key
            try:
                compound_per_chapter[occurrence["chapter"]].append(compound)
            except:
                compound_per_chapter[occurrence["chapter"]] = [compound]

        # calculate and store the average per chapter
        for chapter in compound_per_chapter:
            compound_per_chapter[chapter] = mean(compound_per_chapter[chapter])
        character["compound_average_per_chapter"] = dict(
            sorted(compound_per_chapter.items(), key=lambda item: int(item[0])))

        # calculate and store the average entire book
        compound_average_entire_book = mean(compound_entire_book)
        character["compound_average_entire_book"] = compound_average_entire_book


# Function to save sentiment analysis results to a JSON file
def save_sentiment_results(character_dicts):
    """
    Save the provided character information dictionaries to a JSON file.

    Args:
        character_dicts (list): A list of dictionaries containing character information.

    Writes:
        Saves the character information to a JSON file named "pride_and_prejudice_MainCharacters_NER.json"
        with proper formatting and encoding.
    """
    # create the file and store the dictionaries as a json
    with open(".\\pride_and_prejudice\\pride_and_prejudice_sentiment.json", "w", encoding="UTF8") as jsonfile:
        json.dump(character_dicts, jsonfile, indent=3)


# Main function
def main():

    #initialize the vader sentiment analyzer
    analyzer = SentimentIntensityAnalyzer()

    # Load the JSON file
    file_path = '.\\pride_and_prejudice\\pride_and_prejudice_MainCharacters_NER.json'

    # open and load the file that came out of part1.py to append it with the sentiment
    with open(file_path, 'r') as file:
        character_dicts = json.load(file)

    # execute the anaylsis
    analyze_sentiment(character_dicts, analyzer)

    # save the results to a new json
    save_sentiment_results(character_dicts)



# Run the main function
if __name__ == "__main__":
    main()
